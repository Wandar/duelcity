# -*- coding: utf-8 -*-
from __future__ import annotations
from annos import *
from KBEDebug import *
from a.Signal import *
from b.Card import *
from a.Effect import *
from a.DuelConstants import *
from Constants import *
from a import CardBuff

class ShortEffect(Effect):
    __IS_SHORT_EFFECT__=True
    NEED_NUM=False
    number_0=0



"""
避难:当此卡因其他卡的效果即将从怪兽区离开时,此卡除外,回合结束时从除外区无视条件特殊召唤,保留离开时的ATK
"""
class Refuge(ShortEffect):
    effType = EFF_TYPE.permanent

    observeSignals = (LOCATION.monsterZone+LOCATION.banish,[Signal.BeforeRemovedByEffect,Signal.TurnEnds])

    AI_HINT = [AI_HINT.permanent]
    EFF_POWER = 1

    shouldSpecialsummonTurn=0

    def y_signal(self,signal:Signal.Signal):
        if self.owner.location==LOCATION.monsterZone and isSignal(signal, Signal.BeforeRemovedByEffect):
            if 0:signal:Signal.BeforeRemovedByEffect=signal

            if self.owner in signal.cardList and signal.reasonEffect and signal.reasonEffect.owner!=self.owner and signal.reasonEffectPeriod!=EFF_PERIOD.costing:
                signal.reasonEffect.addFlagCount(EFF_FLAG.resistFromRemovedByEffect, self.owner)
                self.shouldSpecialsummonTurn=self.game.curTurn
                yield self.y_banishCard(self.owner)
        elif isSignal(signal,Signal.TurnEnds):
            if self.shouldSpecialsummonTurn!=0 and self.game.curTurn==self.shouldSpecialsummonTurn:
                self.shouldSpecialsummonTurn=0
                if self.owner.location==LOCATION.banish:
                    yield self.y_specialSummon(self.owner,ignoreRequirement=True)

# class Hero(Effect):
#     effType = EFF_TYPE.permanent
#
#     observeSignals = (LOCATION.mask_all,[Signal.LeaveField,Signal.TurnEnds,Signal.SpecialSummon])
#
#     AI_HINT = [AI_HINT.eraser]
#     EFF_POWER = 1
#
#     shouldSpecialsummonTurn=0
#     savedHP=0
#
#     shouldSendToGraveTurn=0
#     def y_signal(self,signal:Signal.Signal):
#         if isSignal(signal,Signal.LeaveField,self.owner) and self.shouldSendToGraveTurn==0:
#             if 0:signal:Signal.LeaveField=signal
#             if signal.preHP>0 and signal.reasonEffect:
#                 self.shouldSpecialsummonTurn=self.game.curTurn
#                 self.savedHP=signal.preHP
#         elif isSignal(signal,Signal.TurnEnds):
#             if self.shouldSendToGraveTurn!=0 and self.game.curTurn==self.shouldSendToGraveTurn:
#                 self.shouldSendToGraveTurn=0
#                 self.shouldSpecialsummonTurn=0
#                 if self.owner.location&LOCATION.mask_onField!=0:
#                     yield self.y_sendCardToGrave(self.owner)
#             if self.shouldSpecialsummonTurn!=0 and self.game.curTurn==self.shouldSpecialsummonTurn:
#                 self.shouldSpecialsummonTurn=0
#                 yield self.y_specialSummon(self.owner,isLegal=True)
#         elif isSignal(signal,Signal.SpecialSummon,self.owner):
#             self.shouldSpecialsummonTurn=0
#             if 0:signal:Signal.SpecialSummon=signal
#             if not signal.isLegal:
#                 self.shouldSendToGraveTurn=self.game.curTurn
#             else:
#                 self.shouldSendToGraveTurn=0
#                 if signal.reasonEffect==self and self.owner.isMonsterOnField():
#                     yield self.y_changeCardHP(self.owner,self.savedHP)


    # def y_cost(self,justCheck:bool,signal):
    #     if justCheck:
    #         return True
    #     return True
    #
    # def y_activate(self,justCheck:bool,signal):
    #     if justCheck:
    #         return True
    #     return True


"""
抗性:当此卡因其他卡的效果即将从怪兽区离开时,此卡变为半破状态来代替离开
"""
class Resistance(ShortEffect):
    effType = EFF_TYPE.permanent

    NEED_NUM = True
    observeSignals = (LOCATION.monsterZone, [Signal.BeforeRemovedByEffect])
    def y_signal(self, signal:Signal.BeforeRemovedByEffect):
        if self.owner.isMonsterOnField() and isSignal(signal, Signal.BeforeRemovedByEffect) and self.owner in signal.cardList and signal.reasonEffect and signal.reasonEffect.owner!=self.owner and signal.reasonEffectPeriod!=EFF_PERIOD.costing:
            pass
        else:
            return

        if self.owner.atk > self.owner.defence != 0:
            signal.reasonEffect.addFlagCount(EFF_FLAG.resistFromRemovedByEffect, self.owner)
            yield self.owner.y_becomeHalfLife()


"""
魔法免疫
"""
class SpellImmunity(ShortEffect):
    effType = EFF_TYPE.permanent

    observeSignals = (LOCATION.monsterZone,[Signal.AttachMonsterZone,Signal.DetachMonsterZone])

    def y_signal(self,signal):
        if isSignal(signal,Signal.AttachMonsterZone,self.owner):
            yield self.y_addImmunityBuffToCard(self.owner,IMMUNITY_MASK.spell,EFF_DURATION.fromSource,self.effUniID)
        elif isSignal(signal,Signal.DetachMonsterZone,self.owner):
            yield self.y_removeBuffEffectSource(self.owner,self.effUniID)

"""
魔法陷阱免疫
"""
class SpellTrapImmunity(ShortEffect):
    effType = EFF_TYPE.permanent

    observeSignals = (LOCATION.monsterZone,[Signal.AttachMonsterZone,Signal.DetachMonsterZone])

    def y_signal(self,signal):
        if isSignal(signal,Signal.AttachMonsterZone,self.owner):
            yield self.y_addImmunityBuffToCard(self.owner,IMMUNITY_MASK.spell+IMMUNITY_MASK.trap,EFF_DURATION.fromSource,self.effUniID)
        elif isSignal(signal,Signal.DetachMonsterZone,self.owner):
            yield self.y_removeBuffEffectSource(self.owner,self.effUniID)

"""
效果伤害免疫
"""
class EffectDamageImmunity(ShortEffect):
    effType = EFF_TYPE.permanent


"""
自临:此卡无法被通常召唤也无法被其他卡的效果特殊召唤
"""
class SelfDescend(ShortEffect):
    # Marker short effect (无法特召): a card with it cannot be Normal Summoned, nor Special
    # Summoned by a FOREIGN card's effect. Own-effect / ignoreRequirement / player-initiated
    # summons are still allowed. Read in Card.checkBuffCanSpecialSummon / checkBuffCanNormalSummon.
    pass

"""
苏生限制:此卡被其他卡的效果召唤时,此卡变为半破状态
"""
class RevivalRestriction(ShortEffect):
    # RevivalRestriction (苏生限制): does NOT block summoning. Instead, when this card is summoned
    # by a FOREIGN card's effect, it immediately becomes half-broken (its ATK drops to its DEF).
    # Handled in y_signal below (own-effect / normal / player summons are unaffected).
    effType = EFF_TYPE.permanent
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.permanent]
    def y_signal(self, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return
        de = self.game.getDealingEffect()
        effect = de[1] if de else None
        if effect and effect.owner is not self:
            yield self.owner.y_becomeHalfLife()

"""
献祭禁止
"""
class CantBeTributed(ShortEffect):
    # Marker short effect: a card with it cannot be tributed (released / used as tribute).
    # Detected in Card.checkBuffCanTribute via getEffect('CantBeTributed');
    # no buff and no signal observing needed (same marker style as Pierce/Protected).
    pass


"""
迟缓:召唤的回合无法攻击
"""
class Slow(ShortEffect):
    effType = EFF_TYPE.permanent
    observeSignals = (LOCATION.monsterZone,[Signal.Summon])
    def y_signal(self,signal):
        if isSignal(signal,Signal.Summon,self.owner):
            yield self.y_changeCardData(self.owner,newAttackTimes=0,effDuration=EFF_DURATION.utilTurnEnds)

"""
复生:被破坏的回合结束阶段临时召唤
"""
class Revive(ShortEffect):
    # Revive: after being destroyed, at that turn's end, special summon this card back with halfBroken + temporary.
    # The temporary-summoned monster is sent to the graveyard at turn end; once per duel.
    effType = EFF_TYPE.permanent
    observeSignals = (LOCATION.grave,[Signal.Destroyed,Signal.TurnEnds])
    shouldSummonTurn=0
    revivedOnce=False
    def y_signal(self,signal):
        if isSignal(signal,Signal.Destroyed,self.owner):
            if not self.revivedOnce:
                self.shouldSummonTurn=self.game.curTurn
        elif isSignal(signal,Signal.TurnEnds):
            if self.shouldSummonTurn!=0 and self.game.curTurn==self.shouldSummonTurn:
                self.shouldSummonTurn=0
                if not self.revivedOnce and self.owner.location==LOCATION.grave and self.freeMonsterSpace()>0:
                    self.revivedOnce=True
                    yield self.y_specialSummon(self.owner,halfBroken=True,buffIDOrList=CARD_BUFF.temporary)


"""
交易:<手牌效果>可以返回卡组然后重新抽一张卡
"""
class Trade(ShortEffect):
    effType = EFF_TYPE.active

    activateLocation = LOCATION.hand

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 1
    def onInit(self):
        self.manaCost=self.getShortEffectTailNumber()


    def y_activate(self,justCheck:bool,signal):
        deckCards=self.searchCards(LOCATION.deck,self.getSide(),CARD_TYPE.all,self)
        if not deckCards:
            return False

        if justCheck:
            return True

        yield self.y_returnCardToDeck(self.owner,returnType=RETURN_TO_DECK.shuffle)
        yield self.y_drawCard()
        return True


#
# class AutoDefend(Effect):
#     effType = EFF_TYPE.instant
#
#     observeSignals = (LOCATION.monsterZone,[Signal.DamageByBattle,Signal.TurnEnds])
#
#     AI_HINT = [AI_HINT.eraser]
#     EFF_POWER = 1
#
#     addedTurn=0
#     def y_signal(self,signal):
#         if isSignal(signal,Signal.TurnEnds) and self.addedTurn==self.game.curTurn:
#             self.addedTurn=0
#             yield self.y_addShield(self.owner,-self.getShortEffectTailNumber(),False)
#
#     def y_activate(self,justCheck:bool,signal:Signal.DamageByBattle):
#         if isSignal(signal,Signal.DamageByBattle) and signal.receiverCard==self.owner and signal.hpDamageNumber>0:
#             battleFinishSignal=signal.battleFinishSignal
#             if battleFinishSignal.receiverCard==self.owner:
#                 pass
#             else:
#                 return False
#         else:
#             return False
#
#         if justCheck:
#             return True
#
#         yield self.y_changeMonsterForm(self.owner,FORM.ranged)
#         success=yield self.y_addShield(self.owner,self.getShortEffectTailNumber())
#         self.addedTurn=self.game.curTurn
#         return success



"""
连击:可以攻击2次
"""
class DoubleAttack(ShortEffect):
    # Combo: this card can attack twice per turn.
    # Mirrors the permanent attack-count pattern (see BattleDragon01): while on the
    # field, set the per-turn attack limit to 2 via a fromSource buff; remove on leave.
    effType = EFF_TYPE.permanent
    observeSignals = (LOCATION.monsterZone, [Signal.AttachMonsterZone, Signal.DetachMonsterZone])
    AI_HINT = [AI_HINT.permanent, AI_HINT.battleBenefit]
    EFF_POWER = 4
    def y_signal(self, signal):
        if isSignal(signal, Signal.DetachMonsterZone, self.owner):
            yield self.y_removeBuffEffectSource(self.owner, self.effUniID)
            return
        if not self.owner.isMonsterOnField():
            return
        yield self.y_changeCardData(self.owner, newAttackTimes=2,
                                    effDuration=EFF_DURATION.fromSource, uniqueSourceID=self.effUniID)

"""
直击:可以直接攻击
"""
class DirectAttack(ShortEffect):
    # Marker: this card can attack the opponent directly even when they control monsters.
    # Read in Game.player_getAttackTargetListOfCard; still blocked by cantDirectAttack buffs.
    pass

"""
无法攻击
"""
class CannotAttack(ShortEffect):
    # Marker: this card cannot declare an attack.
    # Read via Card.checkBuffCanAttack, gated in Card.canBattle(isAttacker).
    pass

"""
效果免疫
"""
class EffectImmune(ShortEffect):
    # Marker: this card is unaffected by a FOREIGN card's effects (own/controller effects still apply).
    # Read in Effect.removeNotAffectedInList, the shared target filter for all effect operations.
    pass

"""
扫射
"""
class Strafe(ShortEffect):
    # Marker: this card's ranged attack hits ALL enemy monsters (each takes rangeAtk damage),
    # instead of only the highest-ATK one. Read in Game.y_rangedAttack.
    pass

"""
回复
"""
class Regeneration(ShortEffect):
    # Regen N (NEED_NUM): at the controller's end phase, if current ATK is below the
    # original ATK, restore ATK by N, capped so it never exceeds the original ATK.
    NEED_NUM = True
    effType = EFF_TYPE.permanent
    observeSignals = (LOCATION.monsterZone, [Signal.TurnEnds])
    AI_HINT = [AI_HINT.permanent]
    EFF_POWER = 2
    def y_signal(self, signal):
        if not isSignal(signal, Signal.TurnEnds):
            return
        if self.game.whoseTurn != self.owner.side:
            return
        if not self.owner.isMonsterOnField():
            return
        origAtk = self.owner.atk_0
        curAtk = self.owner.atk
        if curAtk >= origAtk:
            return
        heal = min(self.number_0, origAtk - curAtk)
        if heal > 0:
            yield self.y_healCard(self.owner, heal)

"""
固定姿态:召唤的回合无法切换表示形式
"""
class FixedStance(ShortEffect):
    # FixedStance: the player cannot manually change this card's battle position on the turn it
    # was summoned. Reuses cantChangeFormThisTurn (the existing position-change gate in
    # Game.player_getChangingMonsterFormOperates), which is reset on turn start.
    effType = EFF_TYPE.permanent
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.permanent]
    def y_signal(self, signal):
        if isSignal(signal, Signal.Summon, self.owner):
            self.owner.cantChangeFormThisTurn = True
        return
        yield

"""
吸能
"""
class Absorb(ShortEffect):
    # Absorb N (NEED_NUM): after this card attacks a monster, it permanently gains N ATK.
    NEED_NUM = True
    effType = EFF_TYPE.permanent
    observeSignals = (LOCATION.monsterZone, [Signal.BattleFinish])
    AI_HINT = [AI_HINT.addAtk]
    def y_signal(self, signal):
        if not isSignal(signal, Signal.BattleFinish):
            return
        if signal.attackerCard is not self.owner:
            return
        if signal.receiverCard is None:
            return
        if not self.owner.isMonsterOnField():
            return
        yield self.y_addCardData(self.owner, attackAdd=self.number_0, effDuration=EFF_DURATION.onceForever)

"""
战意
"""
class WarSpirit(ShortEffect):
    # WarSpirit N (NEED_NUM): when this card declares an attack, it gains N ATK until the battle ends.
    NEED_NUM = True
    effType = EFF_TYPE.permanent
    observeSignals = (LOCATION.monsterZone, [Signal.RequestBattle])
    AI_HINT = [AI_HINT.addAtk]
    def y_signal(self, signal):
        if not isSignal(signal, Signal.RequestBattle):
            return
        if signal.attackerCard is not self.owner:
            return
        yield self.y_addCardData(self.owner, attackAdd=self.number_0, effDuration=EFF_DURATION.utilBattleEnds)

"""
延迟召唤
"""
class DelayedSummon(ShortEffect):
    # DelayedSummon N (NEED_NUM; active + permanent):
    #   A: activate from hand -> place this card face-up in the spell zone as a continuous spell.
    #   Then on each of the controller's standby phases (handled in y_signal), count down; after N
    #   of them, special summon this card from the spell zone (restoring its monster card type).
    NEED_NUM = True
    effType = EFF_TYPE.active | EFF_TYPE.permanent
    activateLocation = LOCATION.hand
    observeSignals = (LOCATION.spellTrapZone, [Signal.StandbyPhase])
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 3
    remaining = 0
    def y_cost(self, justCheck, signal):
        # active activation from hand
        if not (self.owner.location & LOCATION.hand):
            return False
        if self.game.freeSpellSpace(self.getSide()) == 0:
            return False
        if justCheck:
            return True
        return True
    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        successNum = yield self.y_moveCardToSpellZone(self.owner, newCardType=CARD_TYPE.continuousSpell)
        if not successNum:
            return False
        self.remaining = self.number_0
        return True
    def y_signal(self, signal):
        if not isSignal(signal, Signal.StandbyPhase):
            return
        if self.game.whoseTurn != self.getSide():
            return
        if not (self.owner.location & LOCATION.spellTrapZone):
            return
        if self.remaining <= 0:
            return
        self.remaining -= 1
        if self.remaining > 0:
            return
        if self.freeMonsterSpace() == 0:
            self.remaining = 1   # retry next own standby
            return
        yield self.y_specialSummon(self.owner)

"""
空场特召
"""
class EmptyFieldSpecialSummon(ShortEffect):
    # While you control no monsters, you may Special Summon this card from your hand (A).
    effType = EFF_TYPE.active
    activateLocation = LOCATION.hand
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 3
    def y_cost(self, justCheck, signal):
        if self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self):
            return False
        if self.freeMonsterSpace() == 0:
            return False
        if justCheck:
            return True
        return True
    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        yield self.y_specialSummon(self.owner)
        return True

"""
空场额外召唤
"""
class EmptyFieldExtraSummon(ShortEffect):
    # While you control no monsters, you may Extra Summon this card from your hand (A);
    # this consumes one of your per-turn extra-summon allowances.
    effType = EFF_TYPE.active
    activateLocation = LOCATION.hand
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 3
    def y_cost(self, justCheck, signal):
        side = self.getSide()
        if self.searchCards(LOCATION.monsterZone, side, CARD_TYPE.monster, self):
            return False
        if self.freeMonsterSpace() == 0:
            return False
        if self.game.extraSummonCntThisTurn[side] >= self.game.extraSummonCntLimit[side]:
            return False
        if justCheck:
            return True
        return True
    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        self.game.extraSummonCntThisTurn[self.getSide()] += 1
        yield self.y_specialSummon(self.owner)
        return True

"""
招式卡
"""
class SkillCards(ShortEffect):
    # MoveCards N (NEED_NUM): after this card is summoned, once per duel, randomly set N 'move
    # cards' drawn from the named discover pool (POOL_NAME) face-down in your spell/trap zone.
    # NOTE: the pool must be registered first, e.g.
    #   DiscoverPool.instance().registerPool(MoveCards.POOL_NAME, [<move-card keys>])
    NEED_NUM = True
    countLimit = COUNT_LIMIT.onlyOncePerDuel
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 3
    POOL_NAME = '招式卡'
    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        if self.game.freeSpellSpace(self.getSide()) == 0:
            return False
        if justCheck:
            return True
        return True
    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        from DiscoverPool import DiscoverPool
        side = self.getSide()
        n = min(self.number_0, self.game.freeSpellSpace(side))
        if n <= 0:
            return False
        keys = DiscoverPool.instance().getFromPool(self.POOL_NAME, n)
        if not keys:
            return False
        changePlaceSigs = []
        for k in keys:
            if self.game.freeSpellSpace(side) == 0:
                break
            card = self.game.createCard(k, side)
            if not card:
                continue
            t = yield self.game._y_changeCardLocation(card, LOCATION.spellTrapZone, side, FORM.set, ANIM.leaveListToField, summonFx=FX_ID.setCard)
            if t:
                changePlaceSigs.extend(t)
        for s in changePlaceSigs:
            yield self.game.y_sendSignal(s)
        return True

"""
三召
"""
class TripleTribute(ShortEffect):
    # TripleTribute (active): from your hand, tribute 3 of your monsters, then Extra Summon this
    # card (consumes one of your per-turn extra-summon allowances). Independent of y_normalSummon.
    effType = EFF_TYPE.active
    activateLocation = LOCATION.hand
    AI_HINT = [AI_HINT.summoner, AI_HINT.costMonster]
    EFF_POWER = 4
    def y_cost(self, justCheck, signal):
        side = self.getSide()
        if self.game.extraSummonCntThisTurn[side] >= self.game.extraSummonCntLimit[side]:
            return False
        def isTributable(c):
            return c.canTribute()
        monsters = self.searchCards(LOCATION.monsterZone, side, CARD_TYPE.monster, self, isTributable)
        if len(monsters) < 3:
            return False
        if justCheck:
            return True
        selected = yield self.y_selectCards(monsters, TITLE.tribute, side, 3, 3, canCancel=True)
        if not selected or len(selected) < 3:
            return False
        yield self.y_tributeCard(selected, toSummonCard=self.owner)
        return True
    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        if not self.owner.settedMaterialFilter:
            # y_extraSummon requires a material filter; this card pays its cost via the 3 tributes
            # taken in y_cost, so a trivial filter is enough to pass the check (needTribute=False).
            self.owner.settedMaterialFilter = lambda cards: True
        ok = yield self.y_extraSummon(False, self.owner, needTribute=False)
        return ok

"""
无法特召
"""
class CannotSpecialSummon(ShortEffect):
    # Marker (无法特召): literally cannot be Special Summoned, but CAN be Normal Summoned and
    # Extra Summoned. Read in Card.checkBuffCanSpecialSummon (extra summon is exempt).
    pass


"""
穿刺
"""
class Pierce(ShortEffect):
    pass


"""
受保护
"""
class Protected(ShortEffect):
    # Protected (formerly Evasion): this monster can only be chosen as a melee attack
    # target when no non-protected attackable monster remains on its side.
    # Read in Game.player_getAttackTargetListOfCard.
    pass


"""
无法被攻击
"""
class CannotBeAttacked(ShortEffect):
    # Marker: the opponent cannot choose this monster as a (melee) attack target, and it does
    # NOT block direct attacks. Ranged attacks (Game.y_rangedAttack) can still hit it.
    # Read in Game.player_getAttackTargetListOfCard.
    pass
