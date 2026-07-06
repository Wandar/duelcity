# -*- coding: utf-8 -*-
from __future__ import annotations

from util import *
from annos import *
from a.DuelConstants import *
from KBEngine import *

from duelbot.aiBase import DuelAIBase, AI_MSG
from duelbot.aiSupply import CardSupply
from duelbot.aiChoice import ChoiceMixin
from duelbot.aiCombos import COMBOS, evaluateCombos

"""
aiBrain: DuelAINormal — the "entertainment" duel AI.

Big picture per duel:
  1. onDuelStart builds the monster pools; y_initDuelAI asks the human
     player's account-side win/lose pool for this duel's intended outcome
     (self.shouldWin), which every later decision keys off.
  2. Every own turn the base-class loop calls y_think() repeatedly.
     y_think() is THE single readable if/else: each branch first calls a
     y_ helper with justCheck=True, and only when the check passes calls it
     again with justCheck=False to actually do it (project convention, same
     as y_normalSummon). One step per call; returning False ends the turn.
  3. Card sources, in order of preference:
       real hand cards  >  combo (real hand cards)  >  hidden-card morph
     (see aiSupply: the bot never creates cards out of thin air on the field).
"""


class DuelAINormal(ChoiceMixin, DuelAIBase):
    # --- per-duel core state ---
    shouldWin = False          # intended outcome of this duel
    signatureOnField = False   # signature big monster already on board
    duelStartTurn = 0          # game.curTurn when the duel started
    signatureTurnRolled = 6        # randomized turn gate for the signature monster

    # --- monster pools (built from config + D_CARD in onDuelStart) ---
    lowlevelMonsterPool: List[str] = None      # LV<=4
    middleLevelMonsterPool: List[str] = None   # LV5-6
    highLevelMonsterPool: List[str] = None     # LV>=7
    signatureMonstersPool: List[str] = None    # config-first, any level
    extraMonsterPool: List[str] = None         # fusion/synchro etc (whiteMonster)
    POOL_MIN_UNIQUE = 10                       # minimum unique cardKeys per pool
    SIG_LOW_PICK_CHANCE = 0.3                  # chance to fill smalls from signature pool

    # --- battle tuning ---
    losingAttackChance = 0.4   # losing: per-attack proceed chance
    losingMercyHpRatio = 0.5   # losing: below this LP ratio, direct attacks may be skipped

    supply: CardSupply = None

    # ============================================================
    # duel lifecycle
    # ============================================================
    def onDuelStart(self, duel):
        DuelAIBase.onDuelStart(self, duel)
        config = self.getBotConfig()

        self.supply = CardSupply(self)
        self.supply.initFromConfig(config)
        self.initGeneratePool()

        self.duelStartTurn = duel.game.curTurn
        self.turnWaitedAtStart = False

        # Safe defaults; y_initDuelAI overwrites shouldWin asynchronously.
        self.shouldWin = False
        self._outcomeReported = False
        self.signatureOnField = False

        # Signature-monster gate: at least signatureTurn turns, randomized +-
        signatureTurn = config.get("signatureTurn", 6)
        self.signatureTurnRolled = max(1, signatureTurn + random.randint(-1, 2))

        AI_MSG("bot duel start (shouldWin pending y_initDuelAI), signatureTurn=",
               self.signatureTurnRolled)

    def y_initDuelAI(self):
        """Ask the human player's base for this duel's intended outcome.
        No human player (bot vs bot / test) or timeout -> 50/50 roll."""
        sw = None
        playerCE = self._getOutcomePlayerCE()
        if playerCE is not None and getattr(playerCE, "base", None):
            playerCE.base.reqDuelShou(self.duel.duelNode)
            waitResult = yield WaitForCB("onDuelShouldWinResult", 5)
            if waitResult.called and waitResult.args:
                sw = bool(waitResult.args[0])
        if sw is None:
            sw = random.random() < 0.5
        self.shouldWin = bool(sw)
        self._outcomeReported = False
        AI_MSG("y_initDuelAI shouldWin=", self.shouldWin)

    def getBotName(self):
        """MENU_BOTS key of this duel (set by Duel._botName)."""
        try:
            return self.duel._botName
        except Exception:
            return None

    def getBotConfig(self):
        from duelbot.botPack1 import MENU_BOTS
        botName = self.getBotName()
        if botName and botName in MENU_BOTS:
            return MENU_BOTS[botName]
        # Fallback: first config matching our class (legacy behavior)
        for key, cfg in MENU_BOTS.items():
            if cfg.get("aiClass") == self.__class__ or cfg.get("aiClass") == DuelAINormal:
                return cfg
        return {}

    def _getOutcomePlayerCE(self):
        """Human player's AvatarCE (the persistent pool lives on its base);
        None for bot-vs-bot / tests."""
        try:
            return self.duel.getNotBotAvatar(self.getEnemySideTuple()[0])
        except Exception:
            return None

    def onDuelEnd(self, duel):
        # Compare intended vs actual outcome; the player's base compensates
        # the pool when they differ.
        if getattr(self, "_outcomeReported", False):
            return
        self._outcomeReported = True

        try:
            losers = duel._losers or {}
        except Exception:
            return
        if not losers:
            return

        botLost = self.getSide() in losers
        if len(losers) >= 2 and botLost:
            AI_MSG("[outcome] draw, skip")
            return

        playerCE = self._getOutcomePlayerCE()
        if playerCE is not None and getattr(playerCE, "base", None):
            playerCE.base.reportDuelOutcome(self.shouldWin, not botLost)

    def onTurnStart(self):
        self.turnWaitedAtStart = False

    def y_signal(self, signal):
        # Reveal tracking for the CardSupply (cards entering public zones).
        if self.supply is not None:
            self.supply.onSignal(signal)

    # ============================================================
    # THE decision step — all strategy in one readable if/else.
    # Pattern per branch: y_xxx(justCheck=True) to probe, then the same call
    # with justCheck=False to actually do it. Returns True if something was
    # done (the loop calls again); False ends the turn.
    # ============================================================
    def y_think(self):
        game = self.game
        side = self.getSide()
        config = self.getBotConfig()
        turnsPassed = game.curTurn - self.duelStartTurn
        funTurns = config.get("funTurns", 3)
        # Winning bots keep one zone free until the signature monster is out.
        smallLimit = 2 if (self.shouldWin and not self.signatureOnField) else 3
        myMonsterCnt = len(game.monsters[side])

        # ==================== MAIN ====================
        if game.phase != PHASE.battle:
            # -- 1. fun period: small monsters only, hand first --
            if turnsPassed < funTurns:
                if (yield self.y_summonSmallFromHand(True)):
                    return (yield self.y_summonSmallFromHand(False))
                if myMonsterCnt < smallLimit and (yield self.supply.y_fillSmall(True)):
                    return (yield self.supply.y_fillSmall(False))
                return (yield self.y_gotoBattle())

            # -- 2. a combo is fully ready with REAL hand cards: play it --
            readyCombo, almostCombo = evaluateCombos(self)
            if readyCombo:
                ok = yield COMBOS[readyCombo].y_combo(self, False)
                return ok is not False

            # -- 3. winning script: signature monster not out yet --
            if (self.shouldWin and not self.signatureOnField
                    and turnsPassed >= self.signatureTurnRolled):
                # Morph the combo's missing cards into the hand; next think
                # step the combo checks ready and plays itself.
                if almostCombo and self.supply.provideToHand(almostCombo.missing):
                    return True
                if (yield self.supply.y_signatureSummon(True)):
                    return (yield self.supply.y_signatureSummon(False))

            # -- 4. ordinary development from hand --
            if (yield self.y_summonSmallFromHand(True)):
                return (yield self.y_summonSmallFromHand(False))
            if (yield self.y_playSpellFromHand(True)):
                return (yield self.y_playSpellFromHand(False))
            if (yield self.y_setTrapFromHand(True)):
                return (yield self.y_setTrapFromHand(False))

            # -- 5. hand is dry: pad the board via hidden-card morph --
            if myMonsterCnt < smallLimit and (yield self.supply.y_fillSmall(True)):
                return (yield self.supply.y_fillSmall(False))

            return (yield self.y_gotoBattle())

        # ==================== BATTLE ====================
        plan = self.nextAttackPlan()
        if plan is None:
            return False
        if not self.shouldWin and self.mercyShouldSkip(plan):
            return False                       # losing script: pull punches
        attacker, target = plan
        before = attacker.attackCntThisTurn
        yield game.y_player_monsterAttack(attacker, target)
        yield WaitForSeconds(3)
        # If the attack didn't go through, stop instead of re-picking forever.
        return attacker.attackCntThisTurn > before

    # ============================================================
    # y_ helpers used by y_think (justCheck convention)
    # ============================================================
    def y_summonSmallFromHand(self, justCheck):
        """Normal-summon the best LV<=4 monster from the real hand."""
        game = self.game
        if not self.canNormalSummonNow():
            return False
        card = self._bestSmallInHand()
        if card is None:
            return False
        if justCheck:
            return True
        ok = yield game.y_normalSummon(False, card)
        if ok:
            AI_MSG("normal summon from hand:", card.cardKey)
            yield WaitForSeconds(2)
        return ok

    def y_playSpellFromHand(self, justCheck):
        game = self.game
        card = self._firstPlayableSpell()
        if card is None:
            return False
        if justCheck:
            return True
        effList = game.player_getCardCanActivateEffectList(card)
        if not effList:
            return False
        # AI activates the effect directly (the player path errors on
        # multi-effect cards for AIs by design); selectors -> aiChoice.
        yield game.y_activateActiveEffect(effList[0])
        yield WaitForSeconds(2)
        return True

    def y_setTrapFromHand(self, justCheck):
        game = self.game
        side = self.getSide()
        if game.freeSpellSpace(side) <= 0:
            return False
        card = None
        for c in game.hands[side]:
            if c.cardType & CARD_TYPE.trap:
                card = c
                break
        if card is None:
            return False
        if justCheck:
            return True
        ok = yield game.y_player_setCardToSpellZone(False, card)
        if ok:
            yield WaitForSeconds(1.5)
        return ok

    def y_gotoBattle(self):
        """Enter the battle phase only when an attack would actually happen."""
        game = self.game
        if not self._willAttackThisTurn():
            return False
        if game.phase == PHASE.mainphase1:
            yield game.y_changePhase()
            yield WaitForSeconds(random.uniform(1, 2))
        return game.phase == PHASE.battle

    # ============================================================
    # hand pickers
    # ============================================================
    def _bestSmallInHand(self):
        """Best summonable LV<=4 hand monster: signature > prefer-small > ATK."""
        game = self.game
        side = self.getSide()
        cards = [c for c in game.hands[side]
                 if (c.cardType & CARD_TYPE.monster)
                 and 1 <= c.level <= 4
                 and game.checkCanNormalSummon(c)]
        if not cards:
            return None
        sig = self.signatureMonstersPool or []
        small = self.lowlevelMonsterPool or []

        def score(c):
            s = c.getCurNumber()
            if c.cardKey in sig:
                s += 5000
            if c.cardKey in small:
                s += 200
            return s

        cards.sort(key=score, reverse=True)
        return cards[0]

    def _firstPlayableSpell(self):
        game = self.game
        for c in game.hands[self.getSide()]:
            if not (c.cardType & CARD_TYPE.spell):
                continue
            if game.player_getCardCanActivateEffectList(c):
                return c
        return None

    def canNormalSummonNow(self) -> bool:
        game = self.game
        side = self.getSide()
        if game.normalSummonCntThisTurn[side] >= game.normalSummonCntLimit[side]:
            return False
        return game.freeMonsterSpace(side) > 0

    def handCard(self, cardKey) -> Card:
        """First card in hand with this cardKey (combos consume copies in order)."""
        for c in self.game.hands[self.getSide()]:
            if c.cardKey == cardKey:
                return c
        return None

    def missingInHand(self, cardKeys) -> List[str]:
        """Multiset difference: which of `cardKeys` are not covered by the hand."""
        have = {}
        for c in self.game.hands[self.getSide()]:
            have[c.cardKey] = have.get(c.cardKey, 0) + 1
        missing = []
        for k in cardKeys:
            if have.get(k, 0) > 0:
                have[k] -= 1
            else:
                missing.append(k)
        return missing

    # ============================================================
    # battle predicates
    # ============================================================
    def _canAttackFilter(self, card):
        if card.form != FORM.attack:
            return False
        if not card.checkBuffCanAttack():
            return False
        if card.attackCntThisTurn >= card.attackCntLimitPerTurn:
            return False
        return True

    def _willAttackThisTurn(self):
        """Predict whether any attack would actually happen; otherwise the
        brain ends the turn without entering the battle phase."""
        game = self.game
        side = self.getSide()

        attackers = game.searchCards(LOCATION.monsterZone, side, CARD_TYPE.monster,
                                     filterFunc=self._canAttackFilter)
        if not attackers:
            return False

        enemyMonsters = game.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(),
                                         CARD_TYPE.monster)
        if enemyMonsters:
            weakest = min(em.getCurNumber() for em in enemyMonsters)
            return any(m.getCurNumber() > weakest for m in attackers)
        return True

    def nextAttackPlan(self):
        """Return (attackerCard, target) where target is an enemy Card or a
        player side int (direct attack); None when nothing sensible remains."""
        game = self.game
        side = self.getSide()

        attackers = game.searchCards(LOCATION.monsterZone, side, CARD_TYPE.monster,
                                     filterFunc=self._canAttackFilter)
        if not attackers:
            return None

        enemyMonsters = game.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(),
                                         CARD_TYPE.monster)
        random.shuffle(attackers)
        if enemyMonsters:
            # Only pick fights we win: first attacker with a strictly weaker enemy.
            for m in attackers:
                weaker = [e for e in enemyMonsters if e.getCurNumber() < m.getCurNumber()]
                if weaker:
                    return (m, random.choice(weaker))
            return None
        return (attackers[0], random.choice(self.getEnemySideTuple()))

    def mercyShouldSkip(self, plan) -> bool:
        """Losing script: pull punches. Per-attack chance gate, plus extra
        skip probability on direct attacks when the player's LP is low
        (linear: at mercy threshold never skip -> at 0 LP always skip)."""
        game = self.game
        attacker, target = plan

        if random.random() > self.losingAttackChance:
            return True

        if isinstance(target, int):  # direct attack on a player
            ratio = game.LPs[target] / self.duel.INIT_LP
            if ratio < self.losingMercyHpRatio:
                skipChance = 1.0 - ratio / self.losingMercyHpRatio
                if random.random() < skipChance:
                    return True
        return False

    # ============================================================
    # monster pools (config-first, topped up from D_CARD)
    # ============================================================
    def initGeneratePool(self):
        config = self.getBotConfig()
        preferCards = config.get("preferCards") or []
        sigCards = config.get("signatureMonsters") or []
        preferRace = config.get("preferRace")   # single RACE or list/tuple/set

        # Config-first, bucketed by level (duplicates kept as weights)
        self.lowlevelMonsterPool = self._filterCfgCards(preferCards, 1, 4)
        self.middleLevelMonsterPool = self._filterCfgCards(preferCards, 5, 6)
        self.highLevelMonsterPool = self._filterCfgCards(preferCards, 7, 999)
        self.signatureMonstersPool = self._filterCfgCards(sigCards, 1, 999)

        # Extra (fusion/synchro etc): full D_CARD scan
        self.extraMonsterPool = []
        for cardKey, j in D_CARD.items():
            if cardKey == "version":
                continue
            try:
                t = cardTypeStrToInt(j["type"], cardKey)
            except Exception:
                continue
            if (t & CARD_TYPE.monster) and (t & CARD_TYPE.whiteMonster) == CARD_TYPE.whiteMonster:
                self.extraMonsterPool.append(cardKey)

        # Top up to POOL_MIN_UNIQUE unique keys
        self._supplementPool(self.lowlevelMonsterPool, 1, 4, preferRace)
        self._supplementPool(self.middleLevelMonsterPool, 5, 6, preferRace)
        self._supplementPool(self.highLevelMonsterPool, 7, 999, preferRace)
        self._supplementPool(self.signatureMonstersPool, 7, 999, preferRace)

        self.printPools()

    def _filterCfgCards(self, keyList, lvMin=1, lvMax=999):
        """Valid main-deck monster cardKeys from a config list (duplicates kept)."""
        result = []
        for cardKey in keyList:
            j = D_CARD.get(cardKey)
            if not j:
                continue
            try:
                t = cardTypeStrToInt(j["type"], cardKey)
            except Exception:
                continue
            if not (t & CARD_TYPE.monster):
                continue
            if (t & CARD_TYPE.whiteMonster) == CARD_TYPE.whiteMonster:
                continue
            lv = j.get("level", 0)
            if lv < lvMin or lv > lvMax:
                continue
            result.append(cardKey)
        return result

    def _supplementPool(self, pool, lvMin, lvMax, preferRace):
        """Top a pool up to POOL_MIN_UNIQUE unique keys from D_CARD,
        preferRace-filtered first, then relaxed."""
        unique = set(pool)
        need = self.POOL_MIN_UNIQUE - len(unique)
        if need <= 0:
            return

        def _collect(useRace):
            out = []
            for cardKey, j in D_CARD.items():
                if cardKey == "version" or cardKey in unique:
                    continue
                try:
                    t = cardTypeStrToInt(j["type"], cardKey)
                except Exception:
                    continue
                if not (t & CARD_TYPE.monster):
                    continue
                if (t & CARD_TYPE.whiteMonster) == CARD_TYPE.whiteMonster:
                    continue
                lv = j.get("level", 0)
                if lv < lvMin or lv > lvMax:
                    continue
                if useRace and preferRace:
                    try:
                        r = cardRaceStrToInt(j["race"], cardKey)
                    except Exception:
                        continue
                    if isinstance(preferRace, (list, tuple, set)):
                        if r not in preferRace:
                            continue
                    else:
                        if r != preferRace:
                            continue
                out.append(cardKey)
            return out

        candidates = _collect(useRace=True)
        random.shuffle(candidates)
        for ck in candidates:
            if need <= 0:
                break
            pool.append(ck); unique.add(ck); need -= 1

        if need > 0 and preferRace:
            candidates = _collect(useRace=False)
            random.shuffle(candidates)
            for ck in candidates:
                if need <= 0:
                    break
                pool.append(ck); unique.add(ck); need -= 1

    def _isLowLevel(self, cardKey):
        j = D_CARD.get(cardKey)
        if not j:
            return False
        lv = j.get("level", 0)
        return 1 <= lv <= 4

    def _pickLowLevelMonsterKey(self, justPeek=False):
        """Pick a creatable low-level monster cardKey.
        1) With SIG_LOW_PICK_CHANCE, from the LV<=4 part of the signature pool
        2) otherwise from lowlevelMonsterPool
        justPeek=True: deterministic availability check (no randomness)."""
        sigLow = [k for k in (self.signatureMonstersPool or [])
                  if self._isLowLevel(k) and self.supply.canCreateMore(k)]
        if justPeek:
            if sigLow:
                return sigLow[0]
            low = [k for k in (self.lowlevelMonsterPool or []) if self.supply.canCreateMore(k)]
            return low[0] if low else None
        if sigLow and random.random() < self.SIG_LOW_PICK_CHANCE:
            return random.choice(sigLow)
        return self.supply.pickCreatableFromPool(self.lowlevelMonsterPool)

    def printPools(self):
        def _fmt(pool):
            counter = {}
            for k in pool:
                counter[k] = counter.get(k, 0) + 1
            items = ", ".join((k + "x" + str(v)) if v > 1 else k for k, v in counter.items())
            return "total=%d unique=%d [%s]" % (len(pool), len(counter), items)
        AI_MSG("[pool] lowlevelMonsterPool    :", _fmt(self.lowlevelMonsterPool or []))
        AI_MSG("[pool] middleLevelMonsterPool :", _fmt(self.middleLevelMonsterPool or []))
        AI_MSG("[pool] highLevelMonsterPool   :", _fmt(self.highLevelMonsterPool or []))
        AI_MSG("[pool] signatureMonstersPool  :", _fmt(self.signatureMonstersPool or []))


class DuelAI_dragon(DuelAINormal):
    """Subclass example: override getBotConfig to pin a specific config."""
    pass
