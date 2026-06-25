# from Handlers import *
from __future__ import annotations

from KBEngine import *

import UserType
from b.Card import *
from util import *
from annos import *
from a.ManaMgr import ManaMgr
from a import Signal,CardBuff
from a.GameFunc import GameFunc
from card_effects import shortEffects

import traceback

"""
the state of duel and game logic of duel
"""

class Game(Reload, GameFunc):
    def __init__(self, mduel):
        Reload.__init__(self, True, True)
        GameFunc.__init__(self, self, mduel)
        self.duel: Duel = mduel
        self.duelNode: DuelNode = self.duel.duelNode

        self.monsters: Dict[int, List[Card]] = self.makeInitDict([])
        self.spells: Dict[int, List[Card]] = self.makeInitDict([])
        self.hands: Dict[int, List[Card]] = self.makeInitDict([])
        self.decks: Dict[int, List[Card]] = self.makeInitDict([])
        self.extraDecks: Dict[int, List[Card]] = self.makeInitDict([])
        self.graves: Dict[int, List[Card]] = self.makeInitDict([])
        self.banishes: Dict[int, List[Card]] = self.makeInitDict([])

        self.LPs: Dict[int, int] = self.makeInitDict(self.duel.INIT_LP)
        for side,lp in self.LPs.items():
            self.duelNode.c_LPs[side]=lp
            self.duelNode.c_maxLPs[side]=self.duel.INIT_LP
        self.duelNode.c_LPs=self.duelNode.c_LPs
        self.duelNode.c_maxLPs=self.duelNode.c_maxLPs


        # self.manaMgr: ManaMgr = ManaMgr(self)
        # self.manaMax = self.makeInitDict(1)
        # self.mana = self.makeInitDict(1)

        self.handUpperLimit = self.makeInitDict(self.duel.MAX_HAND_CARD)

        self.normalSummonCntThisTurn = self.makeInitDict(0)
        self.extraSummonCntThisTurn = self.makeInitDict(0)
        self.normalSummonCntLimit = self.makeInitDict(1)
        self.extraSummonCntLimit = self.makeInitDict(1)

        self.curTurn = 1

        self.playerBuffs: Dict[int, List[PlayerBuff]] = self.makeInitDict([])

        # self.coins = {1: 0, 2: 0}  #some monster effects need coin

        #effect######################
        self._signalNameToEffectLists: Dict[
            str, List[Effect]] = {}  #key is signal's classname,stored effects are all trigger or instant type
        self._signalNameToEffectListsPrecheck: Dict[
            str, List[
                Effect]] = {}  #key is signal's classname,stored effects are all trigger or instant type,if observes deck

        self.dealingEffectStack: List[Tuple[EFF_PERIOD, Effect]] = []
        self.isCosting = False
        self.waitingActivateEffects:Dict[int,Effect]={} #effectss already payed cost and waiting for activating

        #trigger effects be triggered
        self.triggerEffectQueue: List[Effect] = []

        self.enterSignalCnt = 0
        self.sendSignalCntThisTurn=0
        self._focusStopSignalRecursive = False

        #############################

        #########################SESSION

        #1 or 2
        self.whoseTurn = 1
        self.whoCanMove: tuple = ()
        self.phase = PHASE.standby

        #player operate
        self.playerop: Tuple[int,OPERATE]= (0,OPERATE.none)

        #battle
        self.curBattleMonsterList: List[Card] = []

        self.effectUseCntThisTurn={} #cardName_effectname:cnt

        ########################################

        # fast check level summon on field
        self._levelSums = self.makeInitDict(0)
        # fast check has tuner monster on field
        self._hasOrangeMonster = self.makeInitDict(False)
        self._buffedCards: Dict[int, Card] = {}
        # deal signals reception when card leaves somewhere
        self._leaveLocationEffectList = []

    def makeInitDict(self,value):
        a = {}
        for side in self.duel.avatars:
            a[side] = copy.copy(value)
        return a


    """
    decks: {1:{"a":[],"b":[],"c":[]}}
    """

    def parseDecks(self, decks: Dict[int, Union[Dict, List, Deck]]):
        isSuccess = True
        for side in self.monsters:
            errorSide = 0
            if side not in decks:
                ERROR_MSG("decks not has side ", side)
                errorSide = side
            self.decks[side], self.extraDecks[side] = self._parseDeck(decks[side], side)
            if self.decks[side] == None:
                errorSide = side
            if errorSide:
                avatar = self.duel.avatars[errorSide]
                self.duel.eachPlayerShowNotify(makeStrNoTrans("deckerror", avatar.c_nickName))
                isSuccess = False
            else:
                if self.duel.getPlayerAI(side):
                    for card in self.decks[side] + self.extraDecks[side]:
                        card.hasShown = False

        if isSuccess:
            #make uniID random
            self.duel.shuffleUsedCardsUniID()

        return isSuccess

    # deck example in decks.py
    def _parseDeck(self, deck, side):
        try:
            if type(deck) == dict:
                aList = deck["a"]
                if "b" in deck and type(deck["b"]) == list:
                    bList = deck["b"]
                else:
                    bList = []
            elif type(deck) == list:
                aList = deck
                bList = []
            else:
                deck = deck  #type:Deck
                aList = deck.a
                bList = deck.b

            mainDeck = []
            extraDeck = []
            for cardclass in aList:
                card = self.createCard(cardclass, side)
                if card:
                    card.location = LOCATION.deck
                    mainDeck.append(card)


            for cardclass in bList:
                card = self.createCard(cardclass, side)
                if card:
                    card.location = LOCATION.extraDeck
                    extraDeck.append(card)

            if len(aList) == 0:
                ERROR_MSG("deck not contain a list ", deck)
                return None, None ,None

            mainDeck.reverse()
            return mainDeck, extraDeck
        except Exception as e:
            ERROR_MSG("deck parse exception ", e)
            s = traceback.format_exc()
            arr = s.split('\n')
            for l in arr:
                ERROR_MSG(l)
            ERROR_MSG("failed deck ", deck)
            return None, None,None

    def y_startGameAndDrawStartHands(self, whoseTurn):
        if publish():
            flySpeed = 1
        else:
            flySpeed = 3

        sides = self.hands.keys()

        for side in sides:
            deck = self.decks[side]
            if not self.duel.SKIP_SHUFFLE_DECK:
                random.shuffle(deck)

        for side in sides:
            self.syncCardList(side, LOCATION.deck)
            self.syncCardList(side, LOCATION.extraDeck)
            self.syncCardList(side, LOCATION.grave)
            self.syncCardList(side, LOCATION.banish)
            self.syncCardList(side, LOCATION.hand)

        if self.duel.IS_TEST_PLAY:
            initHandCard=0
        else:
            initHandCard = self.duel.INI_HAND_CARD
        drawNum = self.makeInitDict(initHandCard)
        #draw init hands
        for i in range(max(drawNum.values())):
            for side, deck in self.decks.items():
                if drawNum[side] == 0:
                    continue
                drawNum[side] -= 1
                if len(deck):
                    self.duelNode.playanimPlayerAddCardToHand(side, CardData.getNone(),True, True)
                    card = deck[-1]
                    self.modifyCardList(side, LOCATION.deck, -1, card, ANIM.startGameDrawCard)
                    self.modifyCardList(side, LOCATION.hand, 1, card, ANIM.startGameDrawCard)

        self.whoseTurn = whoseTurn
        self.duelNode.c_whoseTurn = whoseTurn
        self.resetWhoCanMove()
        self.curTurn = 1
        self._setPhase( PHASE.mainphase1)
        self._resetCountersOfEachTurn()

        # self.manaMgr.onTurnStart()#manachange

        self.duel.recalculateAllCardsOperation()
        if not self.duel.IS_TEST_PLAY:
            self.playanimFlyBanner(whoseTurn, "TURN START",str(self.curTurn), flySpeed)
            self.playanimFlyBanner(whoseTurn, "MAIN PHASE1",str(self.curTurn), flySpeed)


    def y_testScene(self):
        ME_START_HAND = ["MountainDragon"]
        ME_START_MONSTER = ["FireDragonRed", "Dragonide", "Wyvern", "Griffin"]
        ME_START_SPELL = []
        ME_START_GRAVE = []
        EN_START_HAND = []
        EN_START_MONSTER = ["StoneBeast"]
        EN_START_SPELL = []
        EN_START_GRAVE = []

        playerSide = self.duel.getNotBotAvatar(1).c_side
        oppoSide = self.getEnemySideTuple(playerSide)[0]

        signals=[]
        if len(ME_START_HAND):
            self.hands[playerSide] = []
            self.syncCardList(playerSide, LOCATION.hand)
            for cardKey in ME_START_HAND:
                card = self.createCard(cardKey, playerSide)
                sigs=yield self._y_changeCardLocation(card, LOCATION.hand)
                signals.extend(sigs)

        if len(EN_START_HAND):
            self.hands[oppoSide] = []
            self.syncCardList(oppoSide, LOCATION.hand)
            for cardKey in EN_START_HAND:
                card = self.createCard(cardKey, oppoSide)
                sigs=yield self._y_changeCardLocation(card, LOCATION.hand)
                signals.extend(sigs)

        for cardKey in ME_START_GRAVE:
            card = self.createCard(cardKey, playerSide)
            sigs=yield self._y_changeCardLocation(card, LOCATION.grave)
            signals.extend(sigs)

        for cardKey in EN_START_GRAVE:
            card = self.createCard(cardKey, oppoSide)
            sigs=yield self._y_changeCardLocation(card, LOCATION.grave)
            signals.extend(sigs)

        for cardKey in ME_START_MONSTER:
            card = self.createCard(cardKey, playerSide)
            sigs=yield self._y_changeCardLocation(card, LOCATION.monsterZone)
            signals.extend(sigs)

        for cardKey in EN_START_MONSTER:
            card = self.createCard(cardKey, oppoSide)
            sigs=yield self._y_changeCardLocation(card, LOCATION.monsterZone)
            signals.extend(sigs)

        for cardKey in ME_START_SPELL:
            card = self.createCard(cardKey, playerSide)
            sigs=yield self._y_changeCardLocation(card, LOCATION.spellTrapZone,FORM.set)
            signals.extend(sigs)

        for cardKey in EN_START_SPELL:
            card = self.createCard(cardKey, oppoSide)
            sigs=yield self._y_changeCardLocation(card, LOCATION.spellTrapZone,FORM.set)
            signals.extend(sigs)

        for sig in signals:
            yield self.y_sendSignal(sig)

        self.duel.recalculateAllCardsOperation()

    def y_startTutorialScene(self):
        ME_START_HAND = ["StoneBeast"]
        ME_START_FIELD = []
        ME_START_GRAVE = []
        EN_START_HAND = ["StoneBeast","Beast_1"]
        EN_START_FIELD =["Beast_1"]
        EN_START_GRAVE = []

        playerSide = self.duel.getNotBotAvatar(1).c_side
        oppoSide = self.getEnemySideTuple(playerSide)[0]

        signals=[]
        if len(ME_START_HAND):
            self.hands[playerSide] = []
            self.syncCardList(playerSide, LOCATION.hand)
            for cardKey in ME_START_HAND:
                card = self.createCard(cardKey, playerSide)
                sigs=yield self._y_changeCardLocation(card, LOCATION.hand)
                signals.extend(sigs)

        if len(EN_START_HAND):
            self.hands[oppoSide] = []
            self.syncCardList(oppoSide, LOCATION.hand)
            for cardKey in EN_START_HAND:
                card = self.createCard(cardKey, oppoSide)
                sigs=yield self._y_changeCardLocation(card, LOCATION.hand)
                signals.extend(sigs)

        for cardKey in ME_START_GRAVE:
            card = self.createCard(cardKey, playerSide)
            sigs=yield self._y_changeCardLocation(card, LOCATION.grave)
            signals.extend(sigs)

        for cardKey in EN_START_GRAVE:
            card = self.createCard(cardKey, oppoSide)
            sigs=yield self._y_changeCardLocation(card, LOCATION.grave)
            signals.extend(sigs)

        for cardKey in ME_START_FIELD:
            card = self.createCard(cardKey, playerSide)
            sigs=yield self._y_changeCardLocation(card, LOCATION.monsterZone)
            signals.extend(sigs)

        for cardKey in EN_START_FIELD:
            card = self.createCard(cardKey, oppoSide)
            sigs=yield self._y_changeCardLocation(card, LOCATION.monsterZone)
            signals.extend(sigs)

        for sig in signals:
            yield self.y_sendSignal(sig)

        self.duel.recalculateAllCardsOperation()


    """
    get all cards that can be seen by players
    """

    def getCardEntityIDList(self):
        result = []
        for side, l in self.monsters.items():
            for card in l:
                if card.entityID != 0:
                    result.append(card.entityID)
        for side, l in self.spells.items():
            for card in l:
                if card.entityID != 0:
                    result.append(card.entityID)
        return result

    def genUniID(self):
        return self.duel.genUniID()

    def clearCantUseLog(self):
        self.duel.cantUseLog = ""

    def CANTUSE_LOG(self, s: str):
        self.duel.cantUseLog = s

    def _resetCountersOfEachTurn(self):
        for side in self.normalSummonCntThisTurn:
            self.normalSummonCntThisTurn[side]=0
        for side in self.extraSummonCntThisTurn:
            self.extraSummonCntThisTurn[side]=0

        #cards
        for side in self.monsters:
            self.extraSummonCntThisTurn[side]=0
            for card in self.monsters[side] + self.spells[side] + self.hands[side] + self.graves[side] + self.banishes[
                side] + self.decks[side]:
                card.onTurnStart()

    def setWhoCanMove(self, sideOrTuple: Union[tuple, int]):
        if type(sideOrTuple) == int:
            sideOrTuple = (sideOrTuple,)
        self.whoCanMove = sideOrTuple
        self.duel._setWhoCanMove(sideOrTuple)


    def resetWhoCanMove(self):
        self.setWhoCanMove(self.whoseTurn)
        self.duel.recalculateAllCardsOperation()

    def _________________clientOperates(self):
        pass

    def y_changePhase(self, flySpeed=1):
        if self.phase == PHASE.mainphase1:
            #to battle
            self._setPhase(PHASE.battle)
            self.playanimFlyBanner(self.whoseTurn, "BATTLE PHASE",str(self.curTurn), flySpeed)
            yield self.y_sendSignal(Signal.ChangePhaseToBattle())
        elif self.phase == PHASE.battle:
            self._setPhase(PHASE.mainphase2)
            self.playanimFlyBanner(self.whoseTurn, "MAIN PHASE2",str(self.curTurn), flySpeed)
            yield self.y_sendSignal(Signal.ChangePhaseToMainPhase2())
        return True

    def appendSignalsByBuffID(self, signals, buffID, card):
        if buffID in (CARD_BUFF.attackAdd, CARD_BUFF.attackChange, CARD_BUFF.attackMulti, CARD_BUFF.rangeAtkAdd,
                      CARD_BUFF.rangeAtkChange, CARD_BUFF.rangeAtkMulti):
            sig = Signal.CardAtkChanged(card)
            signals.append(sig)
        elif buffID in (CARD_BUFF.defenceChange, CARD_BUFF.defenceAdd, CARD_BUFF.defenceMulti):
            sig = Signal.CardDefenceChanged(card)
            signals.append(sig)
        elif buffID in (CARD_BUFF.levelAdd, CARD_BUFF.levelChange):
            sig = Signal.CardLevelChanged(card)
            signals.append(sig)
        elif buffID == CARD_BUFF.attrChange:
            sig = Signal.CardAttrChanged(card)
            signals.append(sig)
        elif buffID == CARD_BUFF.raceChange:
            sig = Signal.CardRaceChanged(card)
            signals.append(sig)

    def makeSignalsNoDuplicate(self, signals) -> List[Signal]:
        uniList = []
        result = []
        for sig in signals:
            if sig.__class__.__name__ in uniList:
                continue
            uniList.append(sig.__class__.__name__)
            result.append(sig)
        return result

    def _y_removeTurnEndsBuffs(self):
        #=====================Card
        removeChangeControllerMonsters=[]
        signals = []
        delUids = []
        for uid, card in self._buffedCards.items():
            isChanged = False
            tempSignals = []
            for i in range(len(card.buffList) - 1, -1, -1):
                buff: CardBuff = card.buffList[i]
                shouldRemove = False
                if buff.duration == EFF_DURATION.utilTurnEnds:
                    if buff.addTurn == self.curTurn:
                        shouldRemove = True
                elif buff.duration == EFF_DURATION.utilNextTurnEnds:
                    if self.curTurn > buff.addTurn:
                        shouldRemove = True
                elif buff.duration == EFF_DURATION.utilMyTurnEnds:
                    if buff.owner.side == self.whoseTurn:
                        shouldRemove = True
                elif buff.duration == EFF_DURATION.utilNextMyTurnEnds:
                    if buff.owner.side == self.whoseTurn and self.curTurn > buff.addTurn:
                        shouldRemove = True
                elif buff.duration == EFF_DURATION.utilOppositeTurnEnds:
                    if buff.owner.side != self.whoseTurn:
                        shouldRemove = True
                if shouldRemove:
                    isChanged = True
                    card._removeBuff(buff)
                    if buff.BUFF_ID==CARD_BUFF.controlled:
                        removeChangeControllerMonsters.append(card)
                    self.appendSignalsByBuffID(tempSignals, buff.BUFF_ID, card)

            if isChanged:
                signals.extend(self.makeSignalsNoDuplicate(tempSignals))
                card.recalBuffsAndOnDataChanged()

            if not card.buffList:
                delUids.append(uid)
        for uid in delUids:
            del self._buffedCards[uid]

        #=======================Player
        for side, buffList in self.playerBuffs.items():
            isChanged = False
            for i in range(len(buffList) - 1, -1, -1):
                buff: PlayerBuff = buffList[i]
                shouldRemove = False
                if buff.duration == EFF_DURATION.utilTurnEnds:
                    if buff.addTurn == self.curTurn:
                        shouldRemove = True
                elif buff.duration == EFF_DURATION.utilNextTurnEnds:
                    if self.curTurn > buff.addTurn:
                        shouldRemove = True
                elif buff.duration == EFF_DURATION.utilMyTurnEnds:
                    if buff.side == self.whoseTurn:
                        shouldRemove = True
                elif buff.duration == EFF_DURATION.utilNextMyTurnEnds:
                    if buff.side == self.whoseTurn and self.curTurn > buff.addTurn:
                        shouldRemove = True
                elif buff.duration == EFF_DURATION.utilOppositeTurnEnds:
                    if buff.side != self.whoseTurn:
                        shouldRemove = True
                if shouldRemove:
                    isChanged = True
                    del buffList[i]
            if isChanged:
                sig = Signal.PlayerBuffChanged()
                sig.side = side
                signals.append(sig)

        for sig in signals:
            yield self.y_sendSignal(sig)

        #=====================monster return to original controller
        for monster in removeChangeControllerMonsters:
            if not monster.hasBuff(CARD_BUFF.controlled):
                yield self.y_changeMonsterController(monster,monster.side_0,isByEffect=False)


    def y_turnEnds(self):
        if publish():
            flySpeed = 1
        else:
            flySpeed = 3

        self.playanimFlyBanner(self.whoseTurn, "TURN END",str(self.curTurn),flySpeed)
        self._setPhase( PHASE.turnend)

        yield self.y_sendSignal(Signal.TurnEnds())

        #CARD_BUFF.temporary
        sendToGraveCards=[]
        for uid, card in self._buffedCards.items():
            if card.hasBuff(CARD_BUFF.temporary):
                sendToGraveCards.append(card)
                card.removeBuffByID(CARD_BUFF.temporary)
        if sendToGraveCards:
            yield self.y_sendCardToGrave(sendToGraveCards)

        yield self._y_removeTurnEndsBuffs()

        if self.duel.hasLoser():
            return False

        self.whoseTurn += 1
        if self.whoseTurn not in self.monsters:
            self.whoseTurn = min(self.monsters.keys())
        self.resetWhoCanMove()
        self.duelNode.c_whoseTurn = self.whoseTurn
        self.curTurn += 1
        self.sendSignalCntThisTurn=0
        self.effectUseCntThisTurn.clear()
        self._resetCountersOfEachTurn()

        # self.manaMgr.onTurnStart() #manachange

        self.duel.regenTimeoutCount()

        self.duel.callBotFunc("onTurnStart")

        self.playanimFlyBanner(self.whoseTurn, "TURN START",str(self.curTurn),flySpeed)

        #Draw Phase
        self._setPhase( PHASE.draw)
        cardList = yield self.y_drawCard(self.whoseTurn, 1, True)
        if cardList:
            sig = Signal.DrawPhase()
            sig.cardList = cardList
            yield self.y_sendSignal(sig)
        else:
            return False #lose

        self._setPhase(PHASE.standby)
        self.playanimFlyBanner(self.whoseTurn, "STANDBY PHASE",str(self.curTurn),flySpeed)
        yield self.y_sendSignal(Signal.StandbyPhase())

        self._setPhase( PHASE.mainphase1)
        self.playanimFlyBanner(self.whoseTurn, "MAIN PHASE1",str(self.curTurn),flySpeed)

        for side in self.monsters:
            self.duel.resetSelected(side)

        return True


    """
    get available and not available operations currently
    
    return availOperations,notavailOperations
    """

    def player_getCardAllOperations(self, card: Card) -> Tuple[List[OPERATE],List[OPERATE]]:
        """
        monster:
            main phase
                changeToDefence=20
                changeToAttack=22
                changeToDefence=24

                summonMelee=30
                summonRanged=32
                extraSummon=33

                activateEffect=101

                attack monster
                direct attack
            battle phase
                attack monster
                direct attack

        spell:
            main phase
                set
            activate

        """

        # if card.isSynchroMonster() and card.location & LOCATION.extraDeck > 0:
        #     allOperates.append(OPERATE.extraSummon)


        # alwaysShowOperates=[]
        # if card.isInHand():
        #     if card.isSpellTrapCard() and self.freeSpellSpace(card.side) != 0:
        #         allOperates.append(OPERATE.setSpell)
        #     elif card.isMonster():
        #         allOperates.append(OPERATE.normalSummon)

        #effects
        # for effID, effect in card.effects.items():
        #     if effect.effType & EFF_TYPE.active > 0:
        #         if effect.activateLocation & card.location > 0:
        #             if not card.isTrap():
        #                 if effect.specificOperate in (
        #                         OPERATE.activateEffect_specialSummon, OPERATE.activateEffect_discard):
        #                     allOperates.append(effect.specificOperate)

        availOperates = []
        notavailOperates=[]


        if card.location == LOCATION.extraDeck:
            canExtraSummon = getBoolYieldReturn(self.y_player_extraSummonFromExtraDeck(True, card, False))
            hasExtraChance=self.extraSummonCntThisTurn[card.side]<self.extraSummonCntLimit[card.side]

            if canExtraSummon and hasExtraChance:
                availOperates.append(OPERATE.extraSummon)
            elif canExtraSummon:
                notavailOperates.append(OPERATE.extraSummon)

            #if extradeck card has no special summon effect,return
            hasSpecialSummonEffect = False
            for effID, effect in card.effects.items():
                if effect.specificOperate == OPERATE.activateEffect_specialSummon and effect.effType & EFF_TYPE.active > 0:
                    hasSpecialSummonEffect = True
                    break

            if not hasSpecialSummonEffect:
                return availOperates,notavailOperates

        if card.isMonster():
            if self.duel.TEST_SUMMON and not card.isOnField():
                availOperates.append(OPERATE.testSummon)
            canNormalSummon=getBoolYieldReturn(self.y_player_normalSummon(True, card,False))
            hasNormalSummonChance=self.normalSummonCntThisTurn[card.side]<self.normalSummonCntLimit[card.side]

            if canNormalSummon and hasNormalSummonChance:
                availOperates.append(OPERATE.normalSummon)
            elif canNormalSummon:
                notavailOperates.append(OPERATE.normalSummon)

            availOperates.extend(self.player_getChangingMonsterFormOperates(card))

            if card.isOnField() and self.checkCanRangedAttack(card):
                availOperates.append(OPERATE.rangedAttack)

        elif card.isSpellTrapCard():
            #check can set to spellZone
            if getBoolYieldReturn(self.y_player_setCardToSpellZone(True, card)):
                availOperates.append(OPERATE.setSpell)
            #check can return a face-down set card back to hand
            if getBoolYieldReturn(self.y_player_returnSetCardToHand(True, card)):
                availOperates.append(OPERATE.returnSetCard)

        canActivateEffectList = self.player_getCardCanActivateEffectList(card)
        activateEffectList=card.getCurLocationActivateEffectList()
        for effect in canActivateEffectList:
            if effect.specificOperate not in availOperates:
                availOperates.append(effect.specificOperate)
        for effect in activateEffectList:
            if effect.specificOperate not in availOperates:
                notavailOperates.append(effect.specificOperate)
        return availOperates,notavailOperates

    def y_player_setCardToSpellZone(self, justCheck, card: Card) -> bool:
        if not self.isMainPhase():
            self.CANTUSE_LOG("canOnlySetInMainPhase")
            return False
        if not card.isSpellTrapCard():
            return False
        if not card.canSetToSpellZone(card.side):
            return False
        if card.location != LOCATION.hand:
            return False

        if self.freeSpellSpace(card.side) == 0:
            return False

        if justCheck:
            return True

        self.playerop=( card.side,OPERATE.setSpell)

        successNum = yield self.y_setCardToSpellZone(card)

        self.playerop=(0,0)
        return successNum != 0

    def y_player_returnSetCardToHand(self, justCheck, card: Card) -> bool:
        #pick up a face-down Spell/Trap from the field back to hand
        if not self.isMainPhase():
            self.CANTUSE_LOG("canOnlyReturnInMainPhase")
            return False
        if not card.isSpellTrapCard():
            return False
        if card.location != LOCATION.spellTrapZone:
            return False
        if card.form & FORM.set == 0:
            return False
        if card.side != self.whoseTurn:
            return False
        #the turn this card was set, it cannot be returned (same rule as activating a just-set card)
        if card.beSetTurn == self.curTurn:
            self.CANTUSE_LOG("cantReturnSetCardThisTurn")
            return False

        if justCheck:
            return True

        self.playerop=(card.side, OPERATE.returnSetCard)
        successNum = yield self.y_returnCardToHand(card)
        self.playerop=(0,0)
        return successNum != 0

    """
    player request to normal summon a card
    
    usage:yield y_player_normalSummon
    """

    def y_player_normalSummon(self, justCheck, card: Card,costSummonChance):
        if card.location != LOCATION.hand:
            return False

        if not self.isMainPhase():
            self.CANTUSE_LOG("canOnlySummonInMainPhase")
            return False

        # if not justCheck:
        #     shouldCancel=yield self.y_checkHasNotAffordableEffect(card.side,[card],Signal.NormalSummon())
        #     if shouldCancel:
        #         return False

        if not justCheck:
            self.playerop=(card.side, OPERATE.normalSummon)

        isSuccess = yield self.y_normalSummon(justCheck, card, card.side, costSummonChance)

        if not justCheck:
            self.playerop=(0,0)
        return isSuccess




    """
    check any card in the cardList cannot afford the mana cost
    """
    def y_checkHasNotAffordableEffect(self,side,cardList,signal):
        return False
        canActivateEffects=[]
        for card in cardList:
            signal.card=card
            for effect in card.effects.values():
                if effect.checkCanActivate(signal,ignoreMana=True):
                    canActivateEffects.append(effect)

        notAffordCard=None
        manaCost=0
        for effect in canActivateEffects:
            manaCost+=effect.manaCost
            if not self.manaMgr.affordable(side,manaCost):
                notAffordCard=effect.owner
                break

        t=makeStrAllTrans("notaffordableManaSummonText","_CARD_KEY_"+notAffordCard.cardKey)
        option=yield self.y_showYesNoPopUp("notaffordableManaSummonTitle",t,side)
        if option==1:
            return True
        return False


    def y_player_extraSummonFromExtraDeck(self, justCheck, card, costSumnonChance) -> bool:
        if not self.isMainPhase():
            self.CANTUSE_LOG("canOnlySummonInMainPhase")
            return False

        if not justCheck:
            self.playerop=(card.side, OPERATE.extraSummon)

        result = yield self.y_extraSummon(justCheck, card, True, costSumnonChance)

        if not justCheck:
            self.playerop=(0,0)

        return result


    """
    get available change form
    """

    def player_getChangingMonsterFormOperates(self, card: Card) -> List[OPERATE]:
        if not card.isInMonsterZone():
            return []
        if card.attackCntThisTurn > 0:
            return []
        if not card.checkBuffCanPlayerChangeForm():
            return []
        if card.cantChangeFormThisTurn:
            return []

        operates = []
        if not card.isDefence():
            if card.canChangeForm(FORM.defence):
                operates.append(OPERATE.changeToDefence)
        elif card.isDefence():
            if card.canChangeForm(FORM.attack):
                operates.append(OPERATE.changeToAttack)

        return operates

    """
    player req change card form,to melee attack or to range attack or to defence
    """

    def y_player_changeMonsterForm(self, card: Card, operate: OPERATE):
        if operate not in self.player_getChangingMonsterFormOperates(card):
            return

        if operate == OPERATE.changeToAttack:
            newForm = FORM.attack
        elif operate == OPERATE.changeToDefence:
            newForm = FORM.defence
        else:
            ERROR_MSG("no operate changeForm")
            return

        if newForm == card.form:
            return

        self.playerop=(card.side, operate)

        card.playerChangedFormCntThisTurn += 1
        yield self.y_changeForm(card, newForm, False)

        self.playerop=(0,0)

    """
    get list of effects can be activated currently
    """

    def player_getCardCanActivateEffectList(self, card: Card) -> [Effect]:
        efflist = []

        sig = Signal.PlayerActivate(card)
        for effID, effect in card.effects.items():
            isSuccess = effect.checkCanActivate(sig)
            if isSuccess:
                efflist.append(effect)
        return efflist

    #if player activate ,set specificOperate
    #if bot activate ,set specificOrder
    def y_player_activateActiveEffect(self, side, card: Card, specificOperate=0):
        if side != card.side:
            return False

        activeEffectList = self.player_getCardCanActivateEffectList(card)

        #delete other effects,only remain effects with specific operations like "discard" "special summon" "tribute"
        if OPERATE.activateEffect < specificOperate < OPERATE.activateEffect_end:
            for i in range(len(activeEffectList) - 1, -1, -1):
                effect = activeEffectList[i]
                if effect.specificOperate != specificOperate:
                    del activeEffectList[i]
        elif specificOperate != 0 and specificOperate != OPERATE.activateEffect:
            WARNING_MSG("y_player_activateActiveEffect specificOperate not legal:", specificOperate)

        effect: Effect = None
        if len(activeEffectList) > 1:
            if self.duel.getPlayerAI(side):
                ERROR_MSG("ai please use y_activateActiveEffect directly")
                effect = activeEffectList[0]
            else:
                specificOrder = yield self.y_selectFromActivateEffects(side, activeEffectList, True)
                if specificOrder >= len(activeEffectList):  #cancelled
                    return False
                effect = activeEffectList[specificOrder]

        elif len(activeEffectList) == 1:
            effect = activeEffectList[0]
        else:
            return False

        self.playerop=(side, OPERATE.activateEffect)
        yield self.y_activateActiveEffect(effect)
        self.playerop=(0,0)
        return True


    #return list of cards[Card] and sides[int]
    def player_getAttackTargetListOfCard(self, card: Card) -> Tuple[[Card], [int]]:
        result = [], []
        side = card.side
        if self.phase not in (PHASE.mainphase1, PHASE.battle):
            return result
        if not card.canBattle(True):
            return result
        if self.whoseTurn != side:
            return result

        if self.duel.INFINITE_BATTLE:
            pass
        elif card.attackCntThisTurn >= card.attackCntLimitPerTurn:
            return result

        if self.hasPlayerBuff(side, PLAYER_BUFF.cantDeclareAttack):
            return result

        cantDirectAttack = self.hasPlayerBuff(side, PLAYER_BUFF.cantDirectAttack)

        for enemySide in self.getEnemySideTuple(side):
            if enemySide == side:
                continue

            notHideMonsters = self.getNotHideMonsterList(enemySide)
            # CannotBeAttacked: cannot be chosen as a melee target and does not block direct attack
            attackableFaceUp = [m for m in notHideMonsters if not m.getEffect(shortEffects.CannotBeAttacked)]
            if attackableFaceUp:
                # Protected: can only be attacked when no non-protected attackable monster remains
                normalMonsters = [m for m in attackableFaceUp if not m.getEffect(shortEffects.Protected)]
                result[0].extend(normalMonsters if normalMonsters else attackableFaceUp)
                # DirectAttack: may hit the player directly even while the enemy has monsters
                if (not cantDirectAttack) and (not card.hasBuff(CARD_BUFF.cantDirectAttack)) and card.getEffect(shortEffects.DirectAttack):
                    result[1].append(enemySide)
            else:
                hideMonsters = self.getHideMonsterList(enemySide)
                result[0].extend(hideMonsters)
                result[1].append(enemySide)
        return result

    def y_player_monsterRangedAttack(self,shooter:Card):
        if self.phase == PHASE.mainphase2:
            return False

        yield self._y_askChangeToBattlePhaseAndShowHand()
        if self.phase != PHASE.battle:
            return False

        isSuccess = yield self.y_rangedAttack(shooter)
        return isSuccess


    #playter request a monster to attack target
    #if target == 1,2 direct attack
    def y_player_monsterAttack(self, attacker: Card, target: Union[int, Card]):
        side = attacker.side
        if attacker == target:
            return False

        if self.phase == PHASE.mainphase2:
            return False

        if self.duel.hasLoser():
            yield WaitForSeconds(1)
            return

        if type(target) == int:  #direct attack
            targetSide = target
            if targetSide not in self.monsters:
                ERROR_MSG("y_player_monsterAttack target=", target)
                return False

            if targetSide not in self.player_getAttackTargetListOfCard(attacker)[1]:
                return False

            yield self._y_askChangeToBattlePhaseAndShowHand()

            if self.phase != PHASE.battle:
                return False

            isSuccess = yield self.y_directAttack(attacker, targetSide, True)
            return isSuccess
        else:
            if not target.isMonster():
                ERROR_MSG("y_client_monsterAttack target not monster card")
                return False
            if not target.isInMonsterZone():
                ERROR_MSG("y_client_monsterAttack target not on monster field")
                return False

            if target not in self.player_getAttackTargetListOfCard(attacker)[0]:
                ERROR_MSG("y_client_monsterAttack target not in avail target list")
                return False

            # cardEntity=target.getCardEntity()
            # if cardEntity:
            #     cardEntity.c_playanimBeSelected(attacker.side)

            yield self._y_askChangeToBattlePhaseAndShowHand()
            if self.phase != PHASE.battle:
                return False

            isSuccess = yield self.y_battle(attacker, target, True)
            return isSuccess

    def _y_askChangeToBattlePhaseAndShowHand(self):
        #avatar anim
        avatarAnim=AVATAR_ANIM.attackCommand
        percent=random.random()
        if percent<0.5:
            avatarAnim=AVATAR_ANIM.attackCommand
        elif percent<0.65:
            avatarAnim=AVATAR_ANIM.attackCommand1
        elif percent<0.85:
            avatarAnim=AVATAR_ANIM.attackCommand2
        elif percent<1:
            avatarAnim=AVATAR_ANIM.attackCommand3

        #change phase first
        if self.phase == PHASE.mainphase1:
            # option = yield self.duel.y_showPopup("shouldChangeToBattleTitle", "shouldChangeToBattle", self.whoseTurn,["YES"], 0,"NO")
            option = yield self.duel.y_showPopup("shouldAttack", "", self.whoseTurn,["YES"], 0,"NO",POPUP_TYPE.askbattle)
            if option == 0:
                self.duelNode.playanimAvatarAnim(self.whoseTurn,avatarAnim )
                yield self.y_changePhase()
        elif self.phase==PHASE.battle:
            self.duelNode.playanimAvatarAnim(self.whoseTurn,avatarAnim )

    def ______________________clientOperatesEnd(self):
        pass

    def _________________________basicOperates(self):
        pass

    def BATTLE_MSG(self, *s):
        if True:
            DEBUG_MSG(s)

    def checkCanRangedAttack(self,attacker:Card):
        if attacker.rangeAtk==ATK.none or attacker.rangeAtk==0:
            return False
        if not attacker.isMonsterOnField():
            return False
        if attacker.form!=FORM.attack:
            return False
        if not attacker.getCardEntity():
            return False
        if self.duel.INFINITE_BATTLE:
            pass
        elif attacker.attackCntThisTurn>=attacker.attackCntLimitPerTurn:
            return False
        enemySideTuple=attacker.getEnemySideTuple()
        enemyMonsters=self.searchCards(LOCATION.monsterZone,enemySideTuple,CARD_TYPE.monster,maxFoundNum=1)
        return len(enemyMonsters)!=0


    def y_rangedAttack(self,attacker:Card):
        if not self.checkCanRangedAttack(attacker):
            return False
        enemySideTuple=attacker.getEnemySideTuple()
        enemyMonsters=self.searchCards(LOCATION.monsterZone,enemySideTuple,CARD_TYPE.monster)

        numMax= max(x.getCurNumber() for x in enemyMonsters)
        max_objs = [x for x in enemyMonsters if x.getCurNumber() == numMax]
        if not max_objs:
            return False
        receiver:Card=random.choice(max_objs)
        # Strafe: a ranged attack hits ALL enemy monsters instead of only the highest-ATK one
        isStrafe = bool(attacker.getEffect(shortEffects.Strafe))
        receivers = list(enemyMonsters) if isStrafe else [receiver]

        attackerEntity=attacker.getCardEntity()
        receiverEntity=receiver.getCardEntity()

        if not attackerEntity or not receiverEntity:
            ERROR_MSG("ranged not attackerEntity or not receiverEntity")
            return False

        battlePreData = BattlePreData()
        battlePreData.isRush = False
        battlePreData.preferRanged=True
        battlePreData.hitEntityID = receiver.entityID
        battlePreData.fightBackType = FIGHT_BACK_TYPE.dont

        self.BATTLE_MSG("rangedAttack Start")

        attackerEntity.playanimBattlePre(battlePreData)

        paraID=self.genUniID()
        #attacker battle result
        attackerBattleResult = BattleResult()
        attackerBattleResult.battleResultAnim = ANIM.attackSmoothly
        attackerBattleResult.otherEntityID = receiver.entityID
        attackerBattleResult.hitFx= 0
        attackerBattleResult.number = 0
        attackerBattleResult.numberType = 0
        attackerBattleResult.shouldBroken=False
        attackerBattleResult.shouldDie = False

        attackerEntity.c_cardData = attacker
        attackerEntity.playanimBattleResult(attackerBattleResult,paraID)


        for r in receivers:
            if r.isMonsterOnField():
                yield self.y_damageCard(r,attacker.rangeAtk,FX_ID.none,attacker,paraID)

        attacker.attackCntThisTurn+=1
        return True



    def y_battle(self, attacker: Card, receiver: Card, isPlayerCalled=False):
        if not attacker.canBattle(True):
            self.BATTLE_MSG("attacker cant battle")
            return False

        if not receiver.canBattle(False):
            self.BATTLE_MSG("receiver cant battle")
            return False

        if self.curBattleMonsterList:
            yield self.y_stopBattleAndMovebackToOriginalPos()
        self.BATTLE_MSG("y_battle ", attacker.getName(), receiver.getName())

        #attacker must be first
        self.curBattleMonsterList = [attacker, receiver]

        paraID = self.genUniID()

        #=================================battle pre
        self.BATTLE_MSG("send Battle Pre")




        if receiver.form==FORM.attack:
            battleType=BATTLE_TYPE.attackToAttack
        else:
            battleType=BATTLE_TYPE.attackToDefence

        sig = Signal.RequestBattle()
        sig.card = attacker
        sig.attackerCard = attacker
        sig.receiverCard = receiver
        sig.battleType=battleType
        yield self.y_sendSignal(sig)

        #something happened,and battle cant continue
        if not attacker.canBattle(True) or not receiver.canBattle(False):
            self.curBattleMonsterList.clear()
            self.BATTLE_MSG("something happened,attacker receiver cant battle")
            return False

        self.BATTLE_MSG("send Battle Pre2")


        preForm = attacker.form

        battlePreData = BattlePreData()
        battlePreData.isRush = True
        battlePreData.preferRanged=attacker.preferRanged
        battlePreData.hitEntityID = receiver.entityID
        battlePreData.fightBackType = FIGHT_BACK_TYPE.dont

        if receiver.form == FORM.attack:
            battlePreData.fightBackType = FIGHT_BACK_TYPE.melee

        self.BATTLE_MSG("attacker rush ")



        #monster rush
        attacker.getCardEntity().playanimBattlePre(battlePreData, paraID)


        #======================================in battle,wait for effects

        battleUniID=self.genUniID()

        sig = Signal.InBattle()
        sig.battleUniID=battleUniID
        sig.card = attacker
        sig.attackerCard = attacker
        sig.receiverCard = receiver
        sig.battleType=battleType
        sig.involvedSideList=[attacker.side,receiver.side]
        sig.activatedEffectList=[]
        yield self.y_sendSignal(sig)


        shouldContinue = True

        #attacker form changed,stop attack
        if preForm != attacker.form:
            self.BATTLE_MSG("attacker form changed")
            shouldContinue = False

        #something happened,and battle cant continue
        if not attacker.canBattle(True):
            self.BATTLE_MSG("attacker cant battle")
            shouldContinue = False

        if not receiver.canBattle(False):
            self.BATTLE_MSG("receiver cant battle")
            shouldContinue = False

        attackerEntity = attacker.getCardEntity()
        receiverEntity = receiver.getCardEntity()

        if not attackerEntity:
            self.BATTLE_MSG("attacker disappear")
            shouldContinue = False

        if not receiverEntity:
            self.BATTLE_MSG("receiver disappear")
            shouldContinue = False

        if not shouldContinue:
            self.BATTLE_MSG("battle stop and attacker returns")

            yield self.y_stopBattleAndMovebackToOriginalPos()
            return False

        self.BATTLE_MSG("battle result")


        #attacker battle result
        attackerBattleResult = BattleResult()
        attackerBattleResult.battleResultAnim = ANIM.attackSmoothly
        attackerBattleResult.otherEntityID = receiver.entityID
        attackerBattleResult.hitFx = 0
        attackerBattleResult.number = 0
        attackerBattleResult.numberType = 0
        attackerBattleResult.shouldBroken=False
        attackerBattleResult.shouldDie = False
        #receiver battle result
        receiverBattleResult = BattleResult()
        receiverBattleResult.battleResultAnim = ANIM.attackSmoothly
        receiverBattleResult.otherEntityID = attacker.entityID
        receiverBattleResult.hitFx = 0
        receiverBattleResult.number = 0
        receiverBattleResult.numberType = 0
        receiverBattleResult.shouldBroken=False
        receiverBattleResult.shouldDie = False

        #====================cal damage

        playerDamageSignals=[]
        attackerShouldDie=False
        receiverShouldDie=False

        isCancelled=False
        d=attacker.getData("attackcancelled")
        if d and int(d)==battleUniID:
            #attack cancelled
            isCancelled=True
            attackerBattleResult.battleResultAnim=ANIM.attackCancelled
            receiverBattleResult.battleResultAnim=ANIM.attackCancelled
        else:
            if isPlayerCalled:
                attacker.attackCntThisTurn += 1

            attackerAtk=attacker.atk

            attackerDamageOrder=0 # 0 not die 1 half die 2 over die
            receiverDamageOrder=0
            attackerPlayerTakeDamage=0
            receiverPlayerTakeDamage=0
            battleType:BATTLE_TYPE=0


            # battle logic
            if receiver.form==FORM.attack:
                battleType=BATTLE_TYPE.attackToAttack
                """
                attack vs attack
                """
                attackerBattleResult.hitFx=FX_ID.beHit
                receiverBattleResult.hitFx=FX_ID.beHit

                if attackerAtk>receiver.atk:
                    isOverKill=attackerAtk>=receiver.atk*2
                    if isOverKill:
                        receiverDamageOrder=2
                    else:
                        receiverDamageOrder=1
                    receiverPlayerTakeDamage=attackerAtk-receiver.atk

                elif attackerAtk==receiver.atk:
                    if attackerAtk==receiver.atk==0:
                        pass
                    else:
                        attackerDamageOrder=1
                        receiverDamageOrder=1

                elif attackerAtk<receiver.atk:
                    isBeOverKill=receiver.atk>=attacker.atk*2
                    if isBeOverKill:
                        attackerDamageOrder=2
                    else:
                        attackerDamageOrder=1
                    attackerPlayerTakeDamage=receiver.atk-attackerAtk

            elif receiver.form==FORM.defence:
                battleType=BATTLE_TYPE.attackToDefence
                """
                attack vs defence
                """
                attackerBattleResult.hitFx=FX_ID.none
                receiverBattleResult.hitFx=FX_ID.beHit

                if attackerAtk>receiver.defence:
                    isOverKill=attackerAtk>=receiver.defence*2
                    if isOverKill:
                        receiverDamageOrder=2
                    else:
                        receiverDamageOrder=1
                    if attacker.getEffect(shortEffects.Pierce):
                        receiverPlayerTakeDamage=attackerAtk-receiver.defence
                elif attackerAtk==receiver.defence:
                    pass
                elif attackerAtk<receiver.defence:
                    attackerBattleResult.battleResultAnim=ANIM.getHit
                    attackerBattleResult.hitFx=FX_ID.beHit
                    attackerPlayerTakeDamage=receiver.defence-attackerAtk
            else:
                ERROR_MSG("not implement set card be attacked")


            #check should die and change Atk
            if attackerDamageOrder==1:
                if attacker.hasLife():
                    attackerShouldDie=False
                    yield attacker.y_becomeHalfLife()
                else:
                    attackerShouldDie=True
            elif attackerDamageOrder==2:
                attackerShouldDie=True

            if receiverDamageOrder==1:
                if receiver.hasLife():
                    receiverShouldDie=False
                    yield receiver.y_becomeHalfLife()
                else:
                    receiverShouldDie=True
            elif receiverDamageOrder==2:
                receiverShouldDie=True

            #check player damage
            if attackerPlayerTakeDamage>0:
                attackerPlayerTakeDamage=self.damagePlayer(attacker.side,attackerPlayerTakeDamage,True)
                sig=Signal.PlayerLPLoseByBattle()
                sig.senderCard=receiver
                sig.receiverPlayer=attacker.side
                sig.lpLose=attackerPlayerTakeDamage
                playerDamageSignals.append(sig)

            if receiverPlayerTakeDamage>0:
                receiverPlayerTakeDamage=self.damagePlayer(receiver.side,receiverPlayerTakeDamage,True)

                sig=Signal.PlayerLPLoseByBattle()
                sig.senderCard=attacker
                sig.receiverPlayer=receiver.side
                sig.lpLose=receiverPlayerTakeDamage
                playerDamageSignals.append(sig)

            self.BATTLE_MSG("cal end ",attackerDamageOrder,receiverDamageOrder)

            attackerBattleResult.number=attackerPlayerTakeDamage
            if attackerPlayerTakeDamage>0:
                attackerBattleResult.numberType=NUMBER_TYPE.damagePlayer
            if attackerDamageOrder==1:
                attackerBattleResult.battleResultAnim=ANIM.getHit
            if attackerDamageOrder==2:
                attackerBattleResult.battleResultAnim=ANIM.getHit #over kill
            if attackerShouldDie:
                attackerBattleResult.shouldDie=True
            elif attackerDamageOrder==1:
                attackerBattleResult.shouldBroken=True

            receiverBattleResult.number=receiverPlayerTakeDamage
            if receiverPlayerTakeDamage>0:
                receiverBattleResult.numberType=NUMBER_TYPE.damagePlayer
            if receiverDamageOrder==1:
                receiverBattleResult.battleResultAnim=ANIM.getHit
            if receiverDamageOrder==2:
                receiverBattleResult.battleResultAnim=ANIM.getHit #over kill
            if receiverShouldDie:
                receiverBattleResult.shouldDie=True
            elif receiverDamageOrder==1:
                receiverBattleResult.shouldBroken=True

            #if attacker cant kill receiver,attacker should be pushed back
            if not receiverShouldDie and attackerBattleResult.battleResultAnim==ANIM.attackSmoothly:
                attackerBattleResult.battleResultAnim=ANIM.attackPushBack


        #======================================battle end,send result

        self.BATTLE_MSG("battle end send result")

        attackerEntity.c_cardData = attacker
        receiverEntity.c_cardData = receiver
        attackerEntity.playanimBattleResult(attackerBattleResult, paraID)
        receiverEntity.playanimBattleResult(receiverBattleResult, paraID)

        yield self._y_removeBattleEndBuffs([attacker, receiver])

        if isCancelled:
            return True
        #=====================================BattleEnd signals

        #dead card sent to grave
        changePlaceSignals = []
        deadSignals = []

        if attackerShouldDie:
            t = yield self._y_changeCardLocation(attacker, LOCATION.grave)
            changePlaceSignals.extend(t)
            sig = Signal.DestroyedByBattle(attacker, receiver)
            deadSignals.append(sig)
        if receiverShouldDie:
            t = yield self._y_changeCardLocation(receiver, LOCATION.grave)
            changePlaceSignals.extend(t)
            sig = Signal.DestroyedByBattle(receiver, attacker)
            deadSignals.append(sig)


        battleFinishSignal = Signal.BattleFinish()
        battleFinishSignal.card = attacker
        battleFinishSignal.attackerCard = attacker
        battleFinishSignal.receiverCard = receiver
        battleFinishSignal.battleType=battleType


        for signal in playerDamageSignals:
            yield self.y_sendSignal(signal)

        for signal in changePlaceSignals:
            yield self.y_sendSignal(signal)

        for signal in deadSignals:
            yield self.y_sendSignal(signal)

        yield self.y_sendSignal(battleFinishSignal)

        self.curBattleMonsterList.clear()

        self.BATTLE_MSG("battle function end")
        return True


    def y_directAttack(self, attacker: Card, hitPlayerSide: int = 0, isPlayerCalled=False):
        if not attacker.canBattle(True):
            return False
        if hitPlayerSide not in self.monsters:
            ERROR_MSG("direct attack player side error :", hitPlayerSide)
            return False

        if self.hasPlayerBuff(attacker.side, PLAYER_BUFF.cantDirectAttack):
            return False

        if attacker.hasBuff(CARD_BUFF.cantDirectAttack):
            return False

        if self.curBattleMonsterList:
            yield self.y_stopBattleAndMovebackToOriginalPos()

        self.curBattleMonsterList = [attacker]

        self.BATTLE_MSG("y_directAttack ", attacker.getName())

        paraID = self.genUniID()

        #=================================battle pre


        sig = Signal.RequestBattle()
        sig.card = attacker
        sig.attackerCard = attacker
        sig.receiverPlayer = hitPlayerSide
        sig.battleType=BATTLE_TYPE.directAttack
        yield self.y_sendSignal(sig)

        #something happened,and battle cant continue
        if not attacker.canBattle(True):
            self.curBattleMonsterList.clear()
            self.BATTLE_MSG("attacker cantBattle after request")
            return False


        preForm = attacker.form

        battlePreData = BattlePreData()
        battlePreData.isRush = True
        battlePreData.preferRanged=attacker.preferRanged
        battlePreData.hitEntityID = self.duel.avatars[hitPlayerSide].id
        battlePreData.fightBackType = FIGHT_BACK_TYPE.dont


        self.BATTLE_MSG("attacker start rush")

        #monster rush
        attacker.getCardEntity().playanimBattlePre(battlePreData, paraID)

        #=================================in battle,wait for effects

        battleUniID=self.genUniID()

        sig = Signal.InBattle()
        sig.battleUniID=battleUniID
        sig.card = attacker
        sig.attackerCard = attacker
        sig.receiverPlayer = hitPlayerSide
        sig.battleType=BATTLE_TYPE.directAttack
        sig.involvedSideList=[attacker.side,hitPlayerSide]
        sig.activatedEffectList=[]
        yield self.y_sendSignal(sig)

        shouldContinue = True

        #attacker form changed,stop attack
        if attacker.form!=preForm:
            self.BATTLE_MSG("form changed")
            shouldContinue = False

        #something happened,and battle cant continue
        if not attacker.canBattle(True):
            self.BATTLE_MSG("cant battle after rush")
            shouldContinue = False

        if not shouldContinue:
            yield self.y_stopBattleAndMovebackToOriginalPos()
            return False

        #==================================cal damage

        attackerBR = BattleResult()
        attackerBR.battleResultAnim = ANIM.attackSmoothly
        attackerBR.otherEntityID = self.duel.avatars[hitPlayerSide].id
        attackerBR.hitFx = 0
        attackerBR.number = 0
        attackerBR.numberType = 0
        attackerBR.shouldBroken=False
        attackerBR.shouldDie = False

        receiverBR = BattleResult()
        receiverBR.battleResultAnim = ANIM.getHit
        receiverBR.otherEntityID = attacker.entityID
        receiverBR.hitFx = FX_ID.beHit
        receiverBR.number = 0
        receiverBR.numberType = NUMBER_TYPE.dontshow
        receiverBR.shouldBroken=False
        receiverBR.shouldDie = False


        d=attacker.getData("attackcancelled")
        isCancelled=False
        if d and int(d)==battleUniID:
            #attack cancelled
            isCancelled=True
            attackerBR.battleResultAnim = ANIM.attackCancelled
            self.BATTLE_MSG("attack canceled")
        else:
            realNum=self.damagePlayer(hitPlayerSide,attacker.atk,True)
            receiverBR.number=realNum
            receiverBR.numberType = NUMBER_TYPE.damagePlayer
            if realNum>0:
                damageSig=Signal.PlayerLPLoseByBattle()
                damageSig.senderCard=attacker
                damageSig.reasonCard=attacker
                damageSig.lpLose=realNum
                damageSig.receiverPlayer=hitPlayerSide
                yield self.y_sendSignal(damageSig)

        #=================================
        self.BATTLE_MSG("attack end")

        attackerEntity = attacker.getCardEntity()
        if attackerEntity:
            attackerEntity.c_cardData = attacker
            attackerEntity.playanimBattleResult(attackerBR, paraID)
        self.duelNode.playanimPlayerBattleResult(hitPlayerSide, receiverBR, paraID)

        yield self._y_removeBattleEndBuffs([attacker])

        if isCancelled:
            return True

        if isPlayerCalled:
            attacker.attackCntThisTurn+=1

        battleFinishSignal = Signal.BattleFinish()
        battleFinishSignal.battleType=BATTLE_TYPE.directAttack
        battleFinishSignal.card = attacker
        battleFinishSignal.attackerCard=attacker
        battleFinishSignal.receiverPlayer = hitPlayerSide
        yield self.y_sendSignal(battleFinishSignal)

        self.curBattleMonsterList.clear()
        return True

    def y_stopBattleAndMovebackToOriginalPos(self):
        self.BATTLE_MSG("stop battle move back to original pos")
        yield self._y_removeBattleEndBuffs(self.curBattleMonsterList)
        paraID = self.genUniID()
        for card in self.curBattleMonsterList:
            cardEntity = card.getCardEntity()
            if cardEntity:
                battleResult = BattleResult()
                battleResult.battleResultAnim = ANIM.attackCancelled
                battleResult.otherEntityID = 0
                battleResult.hitFx= 0
                battleResult.number = 0
                battleResult.numberType = NUMBER_TYPE.dontshow
                battleResult.shouldBroken=False
                battleResult.shouldDie = False
                cardEntity.c_cardData = card
                cardEntity.playanimBattleResult(battleResult, paraID)
        self.curBattleMonsterList.clear()



    def _y_removeBattleEndBuffs(self, cardList):
        signals = []
        delUids = []
        for card in cardList:
            isChanged = False
            tempSignals = []
            for i in range(len(card.buffList) - 1, -1, -1):
                buff: CardBuff = card.buffList[i]
                if buff.duration == EFF_DURATION.utilBattleEnds:
                    isChanged = True
                    card._removeBuff(buff)
                    self.appendSignalsByBuffID(tempSignals, buff.BUFF_ID, card)

            if isChanged:
                signals.extend(self.makeSignalsNoDuplicate(tempSignals))
                card.recalBuffsAndOnDataChanged()

            if not card.buffList:
                delUids.append(card.uniID)

        for uid in delUids:
            if uid in self._buffedCards:
                del self._buffedCards[uid]


        for sig in signals:
            yield self.y_sendSignal(sig)

    """
    card changes location,don't use this in card's effect
    
    return: [ExitSignal and EnterSignal]
    returned Signals must be called "y_sendSignal" later
    """

    def _y_changeCardLocation(self, card: Card, newLocation: LOCATION, newSide=0, newForm=FORM.none,
                              leaveListAnim: ANIM = 0, enterListAnim: ANIM = 0, summonFx: FX_ID = 0,
                              returnToDeckType: RETURN_TO_DECK = RETURN_TO_DECK.shuffle) -> [Signal.Signal]:

        DUEL_MSG("_y_changeCardLocation:", card.getName(), newLocation)

        if newLocation & (LOCATION.mask_onField + LOCATION.grave + LOCATION.banish) and newForm & FORM.set==0 and newForm!=0:
            card.setShowed()

        #only change form
        if card.location == newLocation and newSide in (0, card.side):
            if card.isMonsterOnField() and newForm != FORM.none:
                WARNING_MSG("_y_changeCardLocation only change form ", card.getName())
                yield self.y_changeForm(card, newForm)
            return []

        preHP=card.defence
        sigs = []
        if card.isOnField():
            if card.location == LOCATION.monsterZone:
                self.monsters[card.side].remove(card)
                sig = Signal.DetachMonsterZone(card)
                sig.side = card.side
                sig.preHP=preHP
                sigs.append(sig)
            else:
                self.spells[card.side].remove(card)
                sig = Signal.DetachSpellZone(card)
                sig.side = card.side
                sigs.append(sig)

            en = card.getCardEntity()
            if en:
                self.duel.cardEntityLeaveField(en)
                card.entityID = 0
            else:
                WARNING_MSG("card onField but no entity ", card.getName())

        elif card.location == LOCATION.none:
            pass
        else:  #leave list
            self.modifyCardList(card.side, card.location, -1, card, leaveListAnim)
            if card.location == LOCATION.deck:
                sig = Signal.LeaveDeck(card)
            elif card.location == LOCATION.extraDeck:
                sig = Signal.LeaveExtraDeck(card)
            elif card.location == LOCATION.grave:
                sig = Signal.LeaveGrave(card)
            elif card.location == LOCATION.banish:
                sig = Signal.LeaveBanished(card)
            elif card.location == LOCATION.hand:
                sig = Signal.LeaveHand(card)
            else:
                ERROR_MSG("card.location error ", card.location, card.getName())
                sig = None
            if sig:
                sigs.append(sig)

        #leave hand or field,will remove all buffs
        if newLocation & LOCATION.mask_fieldHand == 0:
            card._removeAllBuffs()
            card._recalBuffs()


        preSide = card.side
        if not newSide:
            if card.location & LOCATION.mask_onField and newLocation & LOCATION.mask_onField == 0:
                card.side = card.side_0
            newSide = card.side
        else:
            card.side = newSide

        #checker
        if newLocation == LOCATION.monsterZone:
            if self.freeMonsterSpace(newSide) == 0:
                ERROR_MSG("changeLocation no free monster space ", card.getName())
                newLocation = LOCATION.grave

            if card.cardType_0 & CARD_TYPE.monster == 0:
                ERROR_MSG("spell&trap card shouldn't move to monsterZone:", card.getName())
                newLocation = LOCATION.grave

        elif newLocation == LOCATION.spellTrapZone:
            if self.freeSpellSpace(newSide) == 0:
                ERROR_MSG("changeLocation no free spell space ", card.getName())
                newLocation = LOCATION.grave

        if newLocation == LOCATION.grave and self.hasPlayerBuff(newSide, PLAYER_BUFF.cardBanishedInsteadIntoGrave):
            newLocation = LOCATION.banish

        preLocation = card.location

        if card.hasBuff(CARD_BUFF.voided) and newLocation & LOCATION.mask_onField == 0:
            if preLocation & LOCATION.mask_onField != 0:
                newLocation = LOCATION.banish
            card.removeBuffByID(CARD_BUFF.voided)


        card.preLocation = card.location
        card.location = newLocation

        for playEffUid,waitingActivatingEffect in self.waitingActivateEffects.items():
            if waitingActivatingEffect.owner==card:
                if card.isMonsterOnField():
                    if preLocation==LOCATION.monsterZone and newLocation!=LOCATION.monsterZone:
                        waitingActivatingEffect.addFlagCount(EFF_FLAG.activateCountered)
                        self.duelNode.playanimShowedEffectCardBeCountered(playEffUid)
                elif card.isContinuousOrEquipSpellTrap():
                    if preLocation==LOCATION.spellTrapZone and newLocation!=LOCATION.spellTrapZone:
                        waitingActivatingEffect.addFlagCount(EFF_FLAG.activateCountered)
                        self.duelNode.playanimShowedEffectCardBeCountered(playEffUid)

        if preLocation & LOCATION.mask_onField and newLocation & LOCATION.mask_onField == 0:
            sig = Signal.LeaveField(card)
            sig.preHP=preHP
            sigs.append(sig)
        if preLocation & LOCATION.mask_onField == 0 and newLocation & LOCATION.mask_onField:
            sig = Signal.EnterField(card)
            sig.preLocation = preLocation
            sigs.append(sig)

        if newLocation == LOCATION.none:
            card.cardType = card.cardType_0
            card.form = FORM.none
        elif newLocation == LOCATION.monsterZone:
            self.monsters[newSide].append(card)

            if card.cardType & CARD_TYPE.monster == 0:
                card.cardType = card.cardType_0

            if newForm not in (FORM.attack, FORM.defence,FORM.defenceSet):
                newForm = card.getDefaultForm()
            card.form = newForm
            sig = Signal.AttachMonsterZone(card)
            sig.preLocation=preLocation
            sig.side = card.side
            sigs.append(sig)
        elif newLocation == LOCATION.spellTrapZone:
            self.spells[newSide].append(card)

            #this is not a spell card
            if card.cardType & CARD_TYPE.mask_spellTrap == 0:
                card.cardType = CARD_TYPE.continuousSpell

            if newForm not in (FORM.face, FORM.set):
                newForm = FORM.face
            card.form = newForm
            sig = Signal.AttachSpellZone(card)
            sig.preLocation=preLocation
            sig.side = card.side
            sigs.append(sig)
        else:
            card.cardType = card.cardType_0
            card.form = FORM.none
            self.modifyCardList(newSide, newLocation, 1, card, cardChangeAnim=enterListAnim,
                                returnToDeckType=returnToDeckType)
            if newLocation == LOCATION.deck:
                sig = Signal.EnterDeck(card)
            elif newLocation == LOCATION.extraDeck:
                sig = Signal.EnterExtraDeck(card)
            elif newLocation == LOCATION.grave:
                sig = Signal.EnterGrave(card)
            elif newLocation == LOCATION.banish:
                sig = Signal.EnterBanished(card)
            elif newLocation == LOCATION.hand:
                sig = Signal.EnterHand(card)
            else:
                ERROR_MSG("try to enter illegal location,", newLocation, card.getName())
                newLocation = LOCATION.none
                card.location = newLocation
                sig = None
            if sig:
                sig.preLocation = preLocation
                sigs.append(sig)

        if newLocation & LOCATION.mask_onField > 0:
            yield self.duel.y_cardEntityEnterField(card, summonFx)

        yield card.y_cardChangeLocation(preLocation, preSide)
        if preLocation == LOCATION.monsterZone or card.location == LOCATION.monsterZone:
            self._recalZoneLevelSumAndOrangeMonster()

        for sig in sigs:
            self.makeSignalReason(sig)

        #this is a equip card already equip to someone
        if newLocation != LOCATION.spellTrapZone:
            equipToCard = card.getEquipToCard()
            if equipToCard:
                if card in equipToCard.equipCardList:
                    equipToCard.equipCardList.remove(card)
                card.equipToUID = 0
                sig = Signal.EquipCancel(card)
                sig.equipSpell = card
                sig.monsterCard = equipToCard
                sigs.append(sig)

        #this is a monster card with equip cards
        if newLocation != LOCATION.monsterZone:
            for i in range(len(card.equipCardList) - 1, -1, -1):
                c = card.equipCardList[i]
                # c is a monster card that equiped to another monster
                if c.cardType_0 & CARD_TYPE.monster and c.preLocation == LOCATION.monsterZone and self.freeMonsterSpace(
                        c.side_0) != 0:
                    secondSigs = yield self._y_changeCardLocation(c, LOCATION.monsterZone, c.side_0)
                else:
                    secondSigs = yield self._y_changeCardLocation(c, LOCATION.grave)

                for sig in secondSigs:
                    sig.reasonEffect = None
                    sig.reasonEffectPeriod=0
                    sig.reasonCard = None
                sigs.extend(secondSigs)
                sig = Signal.EquipCancel(c)
                sig.equipSpell = c
                sig.monsterCard = card
                sigs.append(sig)
            card.equipCardList.clear()

        return sigs

    def makeSignalReason(self, sig: Signal.Signal):
        effectperiod, effect = self.getDealingEffect()
        if effect:
            sig.reasonEffect = effect
            sig.reasonEffectPeriod=effectperiod
            sig.reasonCard = effect.owner

    def _________________________basicOperatesEnd(self):
        pass

    def playanimFlyBanner(self, side, banner: str,toptxt="", flySpeed=1.0):
        self.duelNode.playanimFlyBanner(side, banner, toptxt,flySpeed)

    def getAttackMonsterList(self, side):
        l = []
        for m in self.monsters[side]:
            if not m.isDefence():
                l.append(m)
        return l

    def getDefenceMonsterList(self, side):
        l = []
        for m in self.monsters[side]:
            if m.isDefence():
                l.append(m)
        return l

    def getNotHideMonsterList(self,side):
        l = []
        for m in self.monsters[side]:
            if m.flag& CARD_FLAG.hide==0:
                l.append(m)
        return l

    def getHideMonsterList(self, side):
        l = []
        for m in self.monsters[side]:
            if m.flag& CARD_FLAG.hide:
                l.append(m)
        return l

    def ____________________effectRelated(self):
        pass

    def getDealingEffect(self) -> Tuple[EFF_PERIOD, Effect]:
        if len(self.dealingEffectStack):
            return self.dealingEffectStack[-1]
        return None, None

    def getAllActivatingCardNamesStr(self) -> str:
        result = ""
        for p, effect in self.dealingEffectStack:
            result += effect.owner.getName() + ","
        return result

    def getCurrentCardName(self):
        if self.dealingEffectStack:
            return self.dealingEffectStack[-1][1].owner.getName()
        return ""

    """
    effect starts to observe signal, active effect ignore this
    """

    def effectConnect(self, effect: Effect):
        if effect.isConnected:
            return False
        if effect.observeSignals[0] & LOCATION.mask_inDecks != 0:
            theLists = self._signalNameToEffectListsPrecheck
        else:
            theLists = self._signalNameToEffectLists
        for SignalClass in effect.observeSignals[1]:
            signalname = SignalClass.__name__
            if signalname not in theLists:
                theLists[signalname] = []
            l = theLists[signalname]
            if effect not in l:
                l.append(effect)
        effect.isConnected = True
        return True

    def effectDisconnect(self, effect: Effect):
        if not effect.isConnected:
            return False


        if effect.observeSignals[0] & LOCATION.mask_inDecks != 0:
            theLists = self._signalNameToEffectListsPrecheck
        else:
            theLists = self._signalNameToEffectLists

        for SignalClass in effect.observeSignals[1]:
            signalname = SignalClass.__name__
            if signalname not in theLists:
                WARNING_MSG("effectDisconnect signalname not in self._signalNameToEffectLists", signalname,
                            effect.__class__.__name__)
            else:
                l = theLists[signalname]
                if effect in l:
                    l.remove(effect)
                if len(l) == 0:
                    del theLists[signalname]
        effect.isConnected = False
        return True

    def y_activateActiveEffect(self, effect: Effect):
        card = effect.owner
        sig = Signal.PlayerActivate(card)

        canActivate=effect.checkCanActivate(sig)
        if not canActivate:
            return False

        self.dealingEffectStack.append((EFF_PERIOD.costing, effect))
        effUniID = self.genUniID()
        isCostSuccess = yield effect.y_costSuper(False, sig, effUniID)
        self.dealingEffectStack.pop()

        if isCostSuccess:
            self.dealingEffectStack.append((EFF_PERIOD.activating, effect))
            yield effect.y_activateSuper(False, sig, effUniID)
            ASSERT_MSG(self.dealingEffectStack[-1][1] == effect, "self.dealingEffectStack[-1][1]==useEffect")
            self.dealingEffectStack.pop()
        yield effect.y_activateEnd(effUniID)
        return True



    """
    activate trigger and instant effects
    
    signals are in Signal.py
    """

    def y_sendSignal(self, signal):
        if not signal:
            return

        #send to ai bot
        yield self.duel.y_sendSignalToAvatars(signal)

        allObserveEffectList = []
        signalNameList = signal.getSelfAndFatherSignalNames()
        for signalName in signalNameList:
            if signalName in self._signalNameToEffectListsPrecheck:
                #if the effect observes all locations,check first
                for tempEff in self._signalNameToEffectListsPrecheck[signalName]:
                    canCost = yield tempEff.y_cost(True, signal)
                    if not canCost:
                        continue
                    canActivate = yield tempEff.y_activate(True, signal)
                    if not canActivate:
                        continue
                    allObserveEffectList.append(tempEff)

            if signalName in self._signalNameToEffectLists:
                allObserveEffectList.extend(self._signalNameToEffectLists[signalName])

        if not allObserveEffectList:
            #signal not observed
            return

        if self._focusStopSignalRecursive:
            return

        self.sendSignalCntThisTurn+=1
        if self.sendSignalCntThisTurn>=10000:
            ERROR_MSG("too many signals sent this turn")
            return

        if self.enterSignalCnt >= 50:
            ERROR_MSG("Too many recursive in y_sendSignal ", signal.__class__.__name__,
                      self.getAllActivatingCardNamesStr())
            self._focusStopSignalRecursive = True
            return
        if len(self.dealingEffectStack) > 16:
            self._focusStopSignalRecursive = True
            return

        if self.enterSignalCnt > 10:
            WARNING_MSG("self.enterSignalCnt>10")
            yield "wait"

        self.enterSignalCnt += 1

        allObserveEffectList.sort(key=lambda effect: (
            effect.getSide() != self.whoseTurn,#me first
            -effect.owner.location,
            effect.manaCost
        ))

        #send signal
        for effect in allObserveEffectList:
            self.dealingEffectStack.append((EFF_PERIOD.signal, effect))
            yield effect.y_signal(signal)
            self.dealingEffectStack.pop()

        mustInstantList: [Effect] = []
        optionalInstantList: [Effect] = []
        tempTriggerList: [Effect] = []


        beforeActivateSignalEffect=None
        if isSignal(signal, Signal.BeforeActivateEffect):
            beforeActivateSignalEffect=signal.effect

        #check instant and trigger effects
        for effect in allObserveEffectList:
            #whouldnt trigger instant effects when costing
            if effect.effType & EFF_TYPE.instant != 0 and self.isCosting:
                continue

            #cant counter self
            if beforeActivateSignalEffect== effect:
                continue

            isTriggered = yield effect.y_costSuper(True, signal)
            if not isTriggered:
                continue
            canActivate = yield effect.y_activateSuper(True, signal)
            if not canActivate:
                continue

            if effect.effType & EFF_TYPE.optionalInstant == EFF_TYPE.optionalInstant:
                if effect in optionalInstantList:
                    optionalInstantList.remove(effect)
                optionalInstantList.append(effect)
            elif effect.effType & EFF_TYPE.instant != 0:
                if effect in mustInstantList:
                    mustInstantList.remove(effect)
                mustInstantList.append(effect)

            if effect.effType & EFF_TYPE.trigger != 0:
                effect._triggerSignal = signal
                if effect in tempTriggerList:
                    tempTriggerList.remove(effect)
                tempTriggerList.append(effect)

        if self.duel.hasLoser():
            tempTriggerList.clear()
            optionalInstantList.clear()

        tempTriggerList.sort(key=lambda effect: (
            effect.getSide() != self.whoseTurn,
            effect.owner.location,
            effect.manaCost
        ))

        #trigger effects will activate at the end of this operation
        self.addTriggersToQueue(tempTriggerList)

        #sort non-optional instant effects
        mustInstantList.sort(key=lambda effect: (
            effect.getSide() != self.whoseTurn, #me first
            -effect.owner.location
        ))

        l2 = []  #activate effect list
        failedCost = []
        #activate must effects
        for effect in mustInstantList:
            self.dealingEffectStack.append((EFF_PERIOD.costing, effect))
            if effect.checkCanActivate(signal):
                effuniID = self.genUniID()
                isCostSuccess = yield effect.y_costSuper(False, signal, effuniID)
                if isCostSuccess:
                    l2.append((effuniID, effect))
                else:
                    #TODO playanim
                    failedCost.append((effuniID, effect))
            self.dealingEffectStack.pop()

        for v in failedCost:
            yield v[1].y_activateEnd(v[0])

        #activate optinal instant effects
        #enemy choose first
        sides = self.getEnemySideTuple(self.whoseTurn) + self.getAllySideTuple(self.whoseTurn)
        for side in sides:
            queue = []
            for effect in optionalInstantList:
                if effect.getSide() == side and effect.checkCanActivate(signal):
                    queue.append(effect)
            effect = yield self._y_reqPlayerToSelectInstantEffect(side, queue)#type:Effect
            if effect:
                self.dealingEffectStack.append((EFF_PERIOD.costing, effect))
                if effect.checkCanActivate(signal):
                    effuniID = self.genUniID()
                    isCostSuccess = yield effect.y_costSuper(False, signal, effuniID)
                    if isCostSuccess:
                        l2.append((effuniID, effect))
                    else:
                        yield effect.y_activateEnd(effuniID)
                self.dealingEffectStack.pop()


        for i in range(len(l2) - 1, -1, -1):
            effuniID, effect = l2[i]
            self.dealingEffectStack.append((EFF_PERIOD.activating, effect))
            yield effect.y_activateSuper(False, signal, effuniID)
            ASSERT_MSG(self.dealingEffectStack[-1][1] == effect, "self.dealingEffectStack[-1][1]==effect")
            self.dealingEffectStack.pop()
            yield effect.y_activateEnd(effuniID)

        self.enterSignalCnt -= 1
        if self.enterSignalCnt <= 0:
            self._focusStopSignalRecursive = False


    """
    request player to select instant effects
    """

    def _y_reqPlayerToSelectInstantEffect(self, side: int, queue: [Effect]) -> Effect:
        ASSERT_MSG(side in self.hands, "error _y_reqPlayerToSelectInstantEffects sideError")
        if len(queue) == 0:
            return None

        ai=self.duel.getPlayerAI(side)
        if ai:
            effect=yield ai.y_selectInstantEffect(queue)
            return effect


        #only 1 card and (inHand Or OnField)
        if len(queue) == 1:
            effect = queue[0]
            card = effect.owner
            option = yield self.y_showYesNoPopUp(makeStrAllTrans(TITLE.shouldActivate, card.cardKey),
                                                 effect.getDescribe(), side)
            if option == 0:
                return effect
            else:
                return None
        else:
            cardQueue = []
            for eff in queue:
                cardQueue.append(eff.owner)

            #if only 1,show Yes or No,if multi, arrange
            option, resultList = yield self.duel.y_showCardSelectorPanel(cardQueue, TITLE.pleaseSelectEffectToActivate, side,["OK"], 1, 1,
                                                                         cancelOption="CANCEL")

            if option == 1:  #cancelled
                return None

            if len(resultList):
                return resultList[0]

            return None



    def addTriggersToQueue(self, triggerList: [Effect]):
        for effect in triggerList:
            if effect in self.triggerEffectQueue:
                self.triggerEffectQueue.remove(effect)
            self.triggerEffectQueue.append(effect)

    #solve trigger effects in queue
    def y_solveTriggerQueue(self):
        cnt = 0
        while True:
            if len(self.triggerEffectQueue) == 0:
                break

            cnt += 1
            if cnt > 20:
                cardNameList = [e.owner.getName() for e in self.triggerEffectQueue]
                WARNING_MSG("trigger effect maybe endless loop ", cardNameList)
                break

            mustTriggerQueue = []
            optionalTriggerQueue = []
            for effect in self.triggerEffectQueue:
                if effect.effType & EFF_TYPE.optionalTrigger == EFF_TYPE.optionalTrigger:
                    optionalTriggerQueue.append(effect)
                else:
                    mustTriggerQueue.append(effect)
            self.triggerEffectQueue = []

            for effect in mustTriggerQueue:
                signal = effect.getTriggerSignal()
                if not effect.checkCanActivate(signal):
                    continue
                self.dealingEffectStack.append((EFF_PERIOD.costing, effect))
                effuniID = self.genUniID()
                isCostSuccess = yield effect.y_costSuper(False, signal, effuniID)
                self.dealingEffectStack.pop()
                if isCostSuccess:
                    self.dealingEffectStack.append((EFF_PERIOD.activating, effect))
                    yield effect.y_activateSuper(False, signal, effuniID)
                    ASSERT_MSG(self.dealingEffectStack[-1][1] == effect,
                               "trigger self.dealingEffectStack[-1][1]==effect")
                    self.dealingEffectStack.pop()
                yield effect.y_activateEnd(effuniID)

            sides = self.getAllySideTuple(self.whoseTurn) + self.getEnemySideTuple(self.whoseTurn)
            for side in sides:
                queue = []
                for effect in optionalTriggerQueue:
                    if effect.getSide() == side and effect.checkCanActivate(effect.getTriggerSignal()):
                        queue.append(effect)
                queue = yield self._y_reqPlayerToArrangeOptionalEffectQueue(side, queue)
                for effect in queue:
                    signal = effect.getTriggerSignal()
                    if not effect.checkCanActivate(signal):
                        continue
                    self.dealingEffectStack.append((EFF_PERIOD.costing, effect))
                    effuniID = self.genUniID()
                    isCostSuccess = yield effect.y_costSuper(False, signal, effuniID)
                    self.dealingEffectStack.pop()
                    if isCostSuccess:
                        self.dealingEffectStack.append((EFF_PERIOD.activating, effect))
                        yield effect.y_activateSuper(False, signal, effuniID)
                        ASSERT_MSG(self.dealingEffectStack[-1][1] == effect,
                                   "trigger2 self.dealingEffectStack[-1][1]==effect")
                        self.dealingEffectStack.pop()
                    yield effect.y_activateEnd(effuniID)
        self.triggerEffectQueue = []

        for effect in self._leaveLocationEffectList:
            observeLocation = effect.observeSignals[0]
            if observeLocation & effect.owner.location != 0:
                self.effectConnect(effect)
            else:
                self.effectDisconnect(effect)
        self._leaveLocationEffectList.clear()


    """
    request player to select from multi activate effects
    """

    def y_selectFromActivateEffects(self, side, queue: [Effect], canCancel=False):
        if len(queue) == 0:
            return 10000
        options = []
        for eff in queue:
            options.append(eff.getDescribe())
        defaultResult = 0
        cancelOption=""
        if canCancel:
            cancelOption="CANCEL"
            defaultResult = len(options)
        result = yield self.duel.y_showPopup(TITLE.pleaseSelectEffectToActivate, "", side, options, defaultResult,cancelOption, POPUP_TYPE.longText)
        return result



    """
    request player to arrange multi optional trigger
    """

    def _y_reqPlayerToArrangeOptionalEffectQueue(self, side: int, queue: [Effect]) -> [Effect]:

        ASSERT_MSG(side in self.hands, "error y_reqPlayerToArrangeOptionalEffectQueues sideError")
        if len(queue) == 0:
            return []


        #if queue is same
        # isSame=True
        # uniName=queue[0]._getEffectUniName()
        # loc=queue[0].owner.location
        # thehp=queue[0].owner.hp
        # for effect in queue:
        #     if uniName!=effect._getEffectUniName() or effect.owner.location!=loc or effect.owner.hp!=thehp:
        #         isSame=False
        # if isSame:
        #     queue=[queue[0]]


        ai=self.duel.getPlayerAI(side)
        if ai:
            finalQueue=yield ai.y_arrangeTriggerEffects(queue)
            return finalQueue


        #only 1 card and (inHand Or OnField)
        if len(queue) == 1:
            effect = queue[0]
            card = effect.owner
            option = yield self.y_showYesNoPopUp(makeStrAllTrans(TITLE.shouldActivate, card.cardKey),
                                                 effect.getDescribe(), side)
            if option == 0:
                return queue
            else:
                return []
        else:
            cardQueue = []
            for eff in queue:
                cardQueue.append(eff.owner)

            #TODO legal group

            #if only 1,show Yes or No,if multi, arrange
            option, resultList = yield self.duel.y_showCardSelectorPanel(cardQueue, TITLE.pleaseArrangeEffects, side,["OK"], 0, len(cardQueue),
                                                                         cancelOption="CANCEL", hasOrder=True)

            if option == 1:  #cancelled
                return []

            finalQueue = []
            for card in resultList:
                for eff in queue:
                    if eff in list(card.effects.values()):
                        finalQueue.append(eff)
            return finalQueue

    def ____________________effectRelatedEnd(self):
        pass

    def freeMonsterSpace(self, side):
        return max(MAX_MONSTER - len(self.monsters[side]), 0)

    def freeSpellSpace(self, side):
        return max(MAX_SPELL - len(self.spells[side]), 0)

    def isMainPhase(self):
        if self.phase & PHASE.mainphaseMask != 0:
            return True
        else:
            return False

    def isBattlePhase(self):
        return self.phase == PHASE.battle

    def ____________________basicFunc(self):
        pass

    def checkLevelSumAndOrangeMonster(self, side, needlevel):
        if self._levelSums[side] < needlevel:
            return False
        if not self._hasOrangeMonster[side]:
            return False
        return True

    #used for synchro summon
    def _recalZoneLevelSumAndOrangeMonster(self):
        for side, cardList in self.monsters.items():
            hasOrange = False
            levelSum = 0
            for c in cardList:
                levelSum += c.level
                if not hasOrange and c.isOrangeNamedMonster():
                    hasOrange = True
            self._levelSums[side] = levelSum
            self._hasOrangeMonster[side] = hasOrange

    """
    factory function,the only way to create Card class in duel
    
    keyOrClassOrDict can be cardKey:  cardKey:str or cardClass:Class or {"key":"dog"}
    originalSide:belong to which player
    cardData:additional data
    """

    def createCard(self, keyOrClassOrDict: Union[int, str, Card, StoredCardData, dict], originalSide,
                   cardData: CardData = None) -> Card:
        if not keyOrClassOrDict:
            if cardData != None:
                keyOrClassOrDict = cardData.cardKey
            else:
                ERROR_MSG("no idOrKeyOrClass")
                return None

        key = ""
        if StoredCardData.isSameType(keyOrClassOrDict):
            key = keyOrClassOrDict.getCardKey()
        elif type(keyOrClassOrDict) == str:  #key
            key = keyOrClassOrDict
        elif type(keyOrClassOrDict) == int:  #id
            ERROR_MSG("cardKey should be str")
        elif type(keyOrClassOrDict) == dict:
            cardKey = ""
            if "key" in keyOrClassOrDict:
                cardKey = keyOrClassOrDict["key"]
                if cardKey not in D_CARD:
                    ERROR_MSG("undefined cardKey ", cardKey)
                    cardKey = ""

            if not cardKey:
                ERROR_MSG("not found key in dict")
                return None
            key = cardKey
        else:
            key = getattr(keyOrClassOrDict, "CARD_KEY", "")
            if not key:
                debugCARD_DATA = getattr(keyOrClassOrDict, "CARD_DATA", None)
                if debugCARD_DATA:
                    if "key" not in debugCARD_DATA:
                        ERROR_MSG("debugCARD_DATA not has key", debugCARD_DATA)
                    else:
                        key = debugCARD_DATA["key"]

        if not key:
            ERROR_MSG("createCard error", keyOrClassOrDict)
            return None

        if key not in D_CARD:
            ERROR_MSG("createCard key not in D_CARD,", key)
            return None

        if key not in g_allcardClass:
            if "MONSTER" in D_CARD[key]["type"]:
                Class = NormalMonster
            else:
                ERROR_MSG("not found card class,CARD_KEY=", key)
                return None
        else:
            Class = g_allcardClass[key]

        card = Class(key, self, originalSide)
        card.uniID = self.genUniID()
        self.duel.usedCards[card.uniID] = card
        card.location = LOCATION.none

        if cardData != None:
            pass
        return card

    """
    modify cardlist and send to client
    dont use list functions like self.hands[1].append(card),use this function instead

    change:
                -1:remove 1 card    0:update 1 card    1:add 1 card
    card: the card to be added or removed or modified to the list
    cardChangeAnim:
                the client animation
                
    shuffle:  -1 auto decide 0 dont shuffle 1 should shuffle            
    """

    def modifyCardList(self, side, location: LOCATION, change: int, card: Card, cardChangeAnim: ANIM = 0,
                       changeCardParaID=0, returnToDeckType: RETURN_TO_DECK = RETURN_TO_DECK.shuffle):
        if not ASSERT_MSG(side in self.hands, "changeCardList side error"):
            return
        duelID = self.duel.duelID

        cardList: List[Card] = None
        sendType = 0  #0: only send num 1: only send to me 2: send to all players
        if location == LOCATION.hand:
            cardList = self.hands[side]
            sendType = 1
        elif location == LOCATION.deck:
            cardList = self.decks[side]
            sendType = 0
        elif location == LOCATION.extraDeck:
            cardList = self.extraDecks[side]
            sendType = 1
        elif location == LOCATION.grave:
            cardList = self.graves[side]
            sendType = 2
        elif location == LOCATION.banish:
            cardList = self.banishes[side]
            sendType = 2
        elif location & LOCATION.mask_onField:
            WARNING_MSG("no need to sync field card ", location)
            return
        else:
            ERROR_MSG("modify location error ", location)
            return

        #change list
        if change == 0:
            for i in range(len(cardList)):
                tempCard = cardList[i]
                if tempCard.uniID == card.uniID:
                    cardList[i] = card
            card.location = location
        elif change == 1:
            if card not in cardList:
                if location != LOCATION.deck:
                    cardList.append(card)
                else:
                    if returnToDeckType == RETURN_TO_DECK.shuffle:
                        cardList.append(card)
                        random.shuffle(cardList)
                    elif returnToDeckType == RETURN_TO_DECK.top:
                        cardList.append(card)
                    elif returnToDeckType == RETURN_TO_DECK.bottom:
                        cardList.insert(0, card)
                    else:
                        ERROR_MSG("returnToDeckType no RETURN_TYPE")
                        return
            else:
                ERROR_MSG("add twice ", card.getName())
                return
            card.location = location
        elif change == -1:
            if card not in cardList:
                ERROR_MSG("change==-1 card not in cardList", card.getName(), location)
                return
            else:
                cardList.remove(card)
        else:
            ERROR_MSG("changeCardList change !== 0,1,-1")
            return

        cardListNum = len(cardList)
        if cardListNum > 2000:
            ERROR_MSG("sendNum>2000")

        if location == LOCATION.hand:
            self.duel.avatars[side].setOtherClientsHandCard(self.hands[side])

        sendAvatars = list(self.duel.avatars.values()) + self.duel.watcherList
        for avatar in sendAvatars:
            if sendType == 0:  # only send num
                shouldCard = CardData.getNone()
            elif sendType == 1:  # only send to me
                if avatar.c_side == side and avatar.c_duelID == duelID:
                    shouldCard = card
                else:
                    shouldCard = CardData.getNone()
            else:  # send to all
                shouldCard = card
            avatar.c_modifyDuelCardList(duelID, side, location, change, shouldCard, cardListNum, cardChangeAnim,
                                        changeCardParaID)

    """
    sync whole cardList to client
    
    if receiveSide==0,send to all avatars and watchers
    """

    def syncCardList(self, side, location: LOCATION, receiveSide=0):
        duelID = self.duel.duelID
        cardList = []
        sendType = 0
        if location == LOCATION.hand:
            cardList = self.hands[side]
            sendType = 1
        elif location == LOCATION.deck:
            cardList = self.decks[side]
            sendType = 0
        elif location == LOCATION.extraDeck:
            cardList = self.extraDecks[side]
            sendType = 1
        elif location == LOCATION.grave:
            cardList = self.graves[side]
            sendType = 2
        elif location == LOCATION.banish:
            cardList = self.banishes[side]
            sendType = 2
        elif location & LOCATION.mask_onField:
            WARNING_MSG("no need to sync field card ", location)
            return
        else:
            ERROR_MSG("syncCardList error not found location ", location)
            return

        cardListNum = len(cardList)
        if cardListNum > 20000:
            ERROR_MSG("sendNum>20000")

        if location == LOCATION.hand:
            self.duel.avatars[side].setOtherClientsHandCard(self.hands[side])

        if receiveSide:
            receiveList = [self.duel.avatars[receiveSide]]
        else:
            receiveList = list(self.duel.avatars.values()) + self.duel.watcherList

        for avatar in receiveList:
            if sendType == 0:  # only send num
                shouldCardList = []
            elif sendType == 1:  #only send to me
                if avatar.c_side == side and avatar.c_duelID == duelID:
                    shouldCardList = cardList
                else:
                    shouldCardList = []
            else:  #send to all
                shouldCardList = cardList
            avatar.c_syncDuelCardList(duelID, side, location, shouldCardList, cardListNum)

    def _________________endBasicFunc(self):
        pass

    def _reinitBuffAttr(self, side):
        self.normalSummonCntLimit[side] = 1
        self.handUpperLimit[side] = self.duel.MAX_HAND_CARD

    def hasPlayerBuff(self, side, playerBuffID: PLAYER_BUFF):
        for buff in self.playerBuffs[side]:
            if 0:buff=buff #type:PlayerBuff
            if buff.BUFF_ID == playerBuffID:
                return True
        return False

    def recalPlayerBuff(self, side):
        self._reinitBuffAttr(side)

        fromSourceList = []
        for buff in self.playerBuffs[side]:
            if buff.duration == EFF_DURATION.fromSource:
                fromSourceList.append(buff)
            else:
                buff.onBuff(self)
        for buff in fromSourceList:
            buff.onBuff(self)

        # self._mergeListToBuffs()


    def changeLP(self, side, newLP):
        newLP=limitInt32(newLP)
        self.LPs[side] = newLP
        self.duelNode.c_LPs[side] = newLP
        self.duelNode.c_LPs = self.duelNode.c_LPs
        if self.LPs[side] <= 0:
            self.duel.setLoser(side, LOSE_REASON.LPTo0)

    def _setPhase(self,phase:PHASE):
        self.phase=phase
        self.duelNode.c_phase=phase

    #return true damage
    def damagePlayer(self,side,damageNum,isByBattle)->int:
        newLP=self.LPs[side]-damageNum
        self.changeLP(side,newLP)
        return damageNum


    def getEnemySideTuple(self, side):
        return self.duel.getEnemySideTuple(side)

    def getAllySideTuple(self, side):
        return self.duel.getAllySideTuple(side)

    def logobserve(self):
        DEBUG_MSG(self._signalNameToEffectLists)
        DEBUG_MSG(self._signalNameToEffectListsPrecheck)


    def onDestroy(self):
        GameFunc.onDestroy(self)
