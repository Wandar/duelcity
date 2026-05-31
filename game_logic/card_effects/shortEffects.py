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
当此卡的hp受到伤害时,此卡除外,回合结束时特殊召唤
"""


"""
正规出场的此卡因卡的效果从场上离开时,并且此卡的hp大于0,此卡在回合结束阶段特殊召唤(视为正规出场),保留离开时的hp.当此卡因非正规手段被特殊召唤时,在回合结束阶段此卡送入墓地.此卡无法被原本控制者以外的玩家进行释放
"""

"""
当此卡因其他卡的效果即将从怪兽区离开时,此卡除外,回合结束时从除外区无视条件特殊召唤,保留离开时的hp.注:支付代价不算卡的效果
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


class Berserker(ShortEffect):
    effType = EFF_TYPE.permanent

    observeSignals = (LOCATION.monsterZone, [Signal.DetachMonsterZone])
    def y_signal(self,signal):
        if isSignal(signal,Signal.DetachMonsterZone,self.owner) and not self.owner.isMonsterOnField():
            self.owner.delData("berserberUsed")

class DamageReduction(ShortEffect):
    effType = EFF_TYPE.permanent
    NEED_NUM = True


class Maintance(ShortEffect):
    effType = EFF_TYPE.permanent

    NEED_NUM = True

    observeSignals = (LOCATION.monsterZone,[Signal.AttachMonsterZone,Signal.DetachMonsterZone])

    def y_signal(self,signal):
        if isSignal(signal,Signal.AttachMonsterZone,self.owner):
            yield self.game.y_addMaintance(self.getShortEffectTailNumber())
        elif isSignal(signal,Signal.DetachMonsterZone,self.owner):
            yield self.game.y_removeMaintance(self.getShortEffectTailNumber())

"""
怪兽区的此卡获得魔法免疫
"""
class SpellImmunity(ShortEffect):
    effType = EFF_TYPE.permanent

    observeSignals = (LOCATION.monsterZone,[Signal.AttachMonsterZone,Signal.DetachMonsterZone])

    def y_signal(self,signal):
        if isSignal(signal,Signal.AttachMonsterZone,self.owner):
            yield self.y_addImmunityBuffToCard(self.owner,IMMUNITY_MASK.spell,EFF_DURATION.fromSource,self.effUniID)
        elif isSignal(signal,Signal.DetachMonsterZone,self.owner):
            yield self.y_removeBuffEffectSource(self.owner,self.effUniID)


class SpellTrapImmunity(ShortEffect):
    effType = EFF_TYPE.permanent

    observeSignals = (LOCATION.monsterZone,[Signal.AttachMonsterZone,Signal.DetachMonsterZone])

    def y_signal(self,signal):
        if isSignal(signal,Signal.AttachMonsterZone,self.owner):
            yield self.y_addImmunityBuffToCard(self.owner,IMMUNITY_MASK.spell+IMMUNITY_MASK.trap,EFF_DURATION.fromSource,self.effUniID)
        elif isSignal(signal,Signal.DetachMonsterZone,self.owner):
            yield self.y_removeBuffEffectSource(self.owner,self.effUniID)


class EffectDamageImmunity(ShortEffect):
    effType = EFF_TYPE.permanent

class Slow(ShortEffect):
    effType = EFF_TYPE.permanent
    observeSignals = (LOCATION.monsterZone,[Signal.Summon])
    def y_signal(self,signal):
        if isSignal(signal,Signal.Summon,self.owner):
            yield self.y_changeCardData(self.owner,newAttackTimes=0,effDuration=EFF_DURATION.utilTurnEnds)

class SimpleShield(ShortEffect):
    effType = EFF_TYPE.permanent
    observeSignals = (LOCATION.monsterZone,[Signal.Summon])
    def y_signal(self,signal):
        if isSignal(signal,Signal.Summon,self.owner):
            yield self.y_addShield(self.owner,self.getShortEffectTailNumber())

class Revive(ShortEffect):
    effType = EFF_TYPE.trigger
    countLimit = COUNT_LIMIT.onlyOncePerDuel
    observeSignals = (LOCATION.grave,[Signal.EnterGrave,Signal.TurnEnds])
    enterGraveTurn=0
    def y_signal(self,signal):
        if isSignal(signal,Signal.EnterGrave,self.owner):
            yield self.y_specialSummon(self.owner,hp=1)



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

        thedeckCard=random.choice(deckCards)
        yield self.y_returnCardToDeck(self.owner,returnType=RETURN_TO_DECK.shuffle)
        yield self.y_returnCardToHand(thedeckCard)
        return True


class Dredge(ShortEffect):
    effType = EFF_TYPE.active

    activateLocation = LOCATION

    def y_activate(self,justCheck,signal):
        deckCards=self.game.decks[self.getSide()]
        if not deckCards:
            return False

        if justCheck:
            return True

        l=[]
        for i in range(3):
            l.append(deckCards[len(deckCards)-1-i])

        card=yield self.y_select1Card(l,TITLE.toDeckTop)
        if card:
            deckCards.remove(card)
            deckCards.insert(0,card)

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




class Pierce(ShortEffect):
    pass


"""
战斗复活: T:此卡被战斗破坏的回合结束阶段临时召唤
"""
class BattleRevive(ShortEffect):
    effType = EFF_TYPE.trigger

    observeSignals = (LOCATION.monsterZone,[Signal.TurnEnds])

    activatedTurn=0

    AI_HINT = [AI_HINT.eraser]
    AI_POWER = 1
    def y_signal(self,signal):
        if isSignal(signal,Signal.DestroyedByBattle,self):
            self.activatedTurn=self.game.curTurn

    def y_cost(self,justCheck:bool,signal:Signal.TurnEnds):
        if isSignal(signal,Signal.TurnEnds) and self.activatedTurn==self.game.curTurn and not self.owner.isMonsterOnField():
            pass
        else:
            return

        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True

        yield self.y_specialSummon(self.owner)
        return True