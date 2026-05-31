# -*- coding: utf-8 -*-
from __future__ import annotations
from annos import *
from KBEDebug import *
from a import Signal, fitter
from b.Card import *
from a.Effect import *
from a.DuelConstants import *
from Constants import *


"""
"""


"""
magic

选择一只怪兽+1攻击力直到回合结束

[You have a face-up Spellcaster Type monster on your field]:Destroy 1 Spell/Trap Card on your opponent's field.


"""






"""
1T:<陷阱卡发动完成时>:此卡此回合可以攻击2次
"""
class TrapAttackTwice(Effect):
    effType = EFF_TYPE.trigger

    observeSignals = (LOCATION.monsterZone,[Signal.ActivateTrapFinish])

    isTrapActivated=False

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 1

    def y_cost(self,justCheck:bool,signal):
        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal):
        if isSignal(signal,Signal.ActivateTrapFinish):
            pass
        else:
            return False

        if justCheck:
            return True

        yield self.y_changeCardData(self.owner,newAttackTimes=2,effDuration=EFF_DURATION.utilTurnEnds)
        return True

    def onTurnStart(self):
        self.isTrapActivated=False


"""
1I:<对方怪兽攻击时>:我方回复300LP
"""
class AttackRecover(Effect):
    effType = EFF_TYPE.instant

    observeSignals = (LOCATION.monsterZone,[Signal.InBattle])

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 1
    def y_signal(self,signal):
        pass

    def y_cost(self, justCheck:bool, signal:Signal.InBattle):
        if isSignal(signal, Signal.InBattle) and signal.attackerCard.side in self.getEnemySideTuple():
            pass
        else:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True

        yield self.y_healPlayer(self.getSide(),300)
        return True


"""
1I:<此卡被攻击后>[决斗中只能发动1次]:此卡{DEF}+1000
"""
class GetattackedGainDef(Effect):
    effType = EFF_TYPE.instant

    countLimit = COUNT_LIMIT.onlyOncePerDuel

    observeSignals = (LOCATION.monsterZone,[Signal.BattleFinish])

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 1
    def y_signal(self,signal):
        pass


    def y_activate(self,justCheck:bool,signal:Signal.BattleFinish):
        if isSignal(signal,Signal.BattleFinish) and signal.receiverCard==self.owner and self.owner.isMonsterOnField():
            pass
        else:
            return False

        if justCheck:
            return True

        yield self.y_addCardData(self.owner,defenceAdd=1000)
        return True




"""
1I:<此卡召唤时>:使场上一只怪兽{ATK}+1,{DEF}+1,结束阶段时破坏该怪兽
"""
class SummonAddDestroy(Effect):
    effType = EFF_TYPE.instant

    observeSignals = (LOCATION.monsterZone,[Signal.Summon,Signal.TurnEnds])

    buffedCard:Card=None
    summonTurn=0

    AI_HINT = [AI_HINT.eraser,AI_HINT.botDontUse]
    EFF_POWER = 1
    def y_signal(self,signal):
        if isSignal(signal,Signal.TurnEnds) and self.summonTurn==self.game.curTurn:
            pass
        else:
            return
        if self.buffedCard:
            yield self.y_destroyCard(self.buffedCard)

    def y_activate(self,justCheck:bool,signal):
        if isSignal(signal,Signal.Summon,self.owner):
            pass
        else:
            return False
        monsters=self.searchCards(LOCATION.monsterZone,-1,CARD_TYPE.monster,self)
        if not monsters:
            return False
        if justCheck:
            return True

        self.summonTurn=self.game.curTurn
        target=yield self.y_select1Card(monsters,TITLE.target,self.getSide())
        yield self.y_addCardData(target, attackAdd=1, defenceAdd=1, hpAdd=1)
        self.buffedCard=target
        return True

    def y_locationChange(self,oldSide,oldLocation,newSide,newLocation):
        if newLocation& LOCATION.monsterZone==0:
            self.buffedCard=None
            self.summonTurn=0





"""
1A:<场上效果>[每回合同名1次]:选场上一只怪兽,本回合结束时回复该怪兽HP至满
"""

class EffectRawRestoreEndOfturn(Effect):
    effType = EFF_TYPE.active


    manaCost = 0
    countLimit = COUNT_LIMIT.sameNameOncePerTurn

    enablePlace = LOCATION.mask_all
    observeSignals = (LOCATION.mask_all,[Signal.TurnEnds])

    def filter(self, card):
        pass

    def y_cost(self, justCheck: bool, signal):
        cards = self.searchCards(LOCATION.monsterZone, -1, CARD_TYPE.monster)
        if not cards:
            return False
        if justCheck:
            return True

        target = yield self.y_select1Card(cards, TITLE.auto, self.getSide(), canCancel=True)
        if not target:
            return False
        self.saveTarget1(target)
        return True

    def y_signal(self, signal: Signal.TurnEnds):
        if isSignal(signal, Signal.TurnEnds):
            target=self.getLegalTarget1()
            if target:
                yield self.y_restoreCardHP(target)



"""
1A:<此卡召唤时>:如果手牌中有费用≥5的魔法卡,回复5点LP
"""
class EffectRest(Effect):
    effType = EFF_TYPE.trigger

    observeSignals = (LOCATION.monsterZone,[Signal.AttachMonsterZone])

    def filter(self, card):
        if card.cost >= 5:
            return True
        return False

    def y_activate(self, justCheck: bool, signal: Signal.AttachMonsterZone):
        if not isSignal(signal, Signal.AttachMonsterZone, self.owner):
            return False

        card = self.game.query1Card(LOCATION.hand, self.getSide(), CARD_TYPE.spell, self.filter)
        if not card:
            return False

        if justCheck:
            return True

        yield self.y_healPlayer(self.getSide(), 5)
        return True



"""
1P:<手牌效果>:我方怪兽被破坏时,此卡{ATK}+1,{DEF}+1
"""
class EffectFree(Effect):
    effType = EFF_TYPE.permanent

    enablePlace = LOCATION.hand
    observeSignals = (Signal.DestroyedOnField,)

    def y_signal(self, signal: Signal.DestroyedOnField):
        if isSignal(signal, Signal.DestroyedOnField):
            if signal.card.isMonster() and signal.card.side == self.getSide():
                if self.owner.location == LOCATION.hand:
                    self.owner.addBuffAtkHP(1, 1)



"""
1P:<场上效果>:我方机械族怪兽{ATK}+1,{DEF}+1
"""
class EffectOtherAdd(Effect):
    effType = EFF_TYPE.permanent

    observeSignals = (LOCATION.monsterZone,[Signal.CardRaceChanged, Signal.AttachMonsterZone, Signal.DetachMonsterZone])

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 1
    def y_signal(self,signal):
        if isSignal(signal, Signal.DetachMonsterZone):
            if signal.card==self.owner:
                cards=self.searchCards(LOCATION.mask_onField)
                yield self.y_removeBuffEffectSource(cards,self.effUniID)
            else:
                yield self.y_removeBuffEffectSource(signal.card,self.effUniID)

        def f(card):
            return card.race==RACE.MACHINE

        if isSignal(signal,Signal.CardRaceChanged) and not f(signal.card):
            yield self.y_removeBuffEffectSource(signal.card,self.effUniID)

        if self.owner.isMonsterOnField():
            cards=self.searchCards(LOCATION.monsterZone,self.getSide(),CARD_TYPE.monster,None,f)
            yield self.y_addCardData(cards, 1, 1, effDuration=EFF_DURATION.fromSource, uniqueSourceID=self.effUniID)



"""
1P:<场上效果>:我方场上存在机械族怪兽时,此卡{ATK}+2,{DEF}+2
"""
class EffectAdd2(Effect):
    effType = EFF_TYPE.permanent

    observeSignals = (LOCATION.monsterZone,[Signal.AttachMonsterZone, Signal.DetachMonsterZone, Signal.CardRaceChanged])

    def y_signal(self, signal):
        def f(card):
            return card.race==RACE.MACHINE
        machineList=self.searchCards(LOCATION.monsterZone,self.getSide(),CARD_TYPE.monster,None,f)
        if len(machineList):
            yield self.y_addCardData(self.owner, 2, 2, effDuration=EFF_DURATION.fromSource,
                                     uniqueSourceID=self.effUniID)
        else:
            yield self.y_removeBuffEffectSource(self.owner,self.effUniID)



#1A:<场上效果>:此回合我方怪兽不能直接攻击
class CantDirectAttack(Effect):
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 1
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True

        DEBUG_MSG("active")

        yield self.y_addPlayerBuff(self.getSide(),PLAYER_BUFF.cantDirectAttack,EFF_DURATION.utilTurnEnds)
        return True



#1P:<场上效果>:我方卡本应送入墓地时改为除外
class BanishInsteadGrave(Effect):
    effType = EFF_TYPE.permanent

    AI_HINT = [AI_HINT.botDontUse]
    EFF_POWER = 1
    def y_locationChange(self,oldSide,oldLocation,newSide,newLocation):
        if newLocation==LOCATION.spellTrapZone:
            yield self.y_addPlayerBuff(0,PLAYER_BUFF.cardBanishedInsteadIntoGrave,EFF_DURATION.fromSource,self.effUniID)
        else:
            yield self.y_removePlayerBuffEffectSource(0,self.effUniID)


#1T:<此卡近战攻击后>:变为远程表示
class MeleeChangeToRange(Effect):
    effType = EFF_TYPE.active

    observeSignals = (LOCATION.monsterZone,[Signal.BattleFinish])

    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal:Signal.BattleFinish):
        if isSignal(signal,Signal.BattleFinish) and signal.attackerCard==self.owner and signal.isMelee==True and self.owner.isMonsterOnField():
            pass
        else:
            return False

        if justCheck:
            return True

        yield self.y_changeForm(self.owner, FORM.ranged)
        return True

#1T:<我方准备阶段>:此卡{ATK}+100
class StandByAdd(Effect):
    effType = EFF_TYPE.trigger

    observeSignals = (LOCATION.monsterZone,[Signal.StandbyPhase])

    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal:Signal.StandbyPhase):
        if isSignal(signal,Signal.StandbyPhase) and self.game.whoseTurn==self.getSide():
            pass
        else:
            return False

        if justCheck:
            return True

        yield self.y_addCardData(self.owner,100)
        return True

#1T:<此卡攻击怪兽后>:此卡此回合可再攻击1次
class AttackMonsterAgain(Effect):
    effType = EFF_TYPE.trigger

    observeSignals = (LOCATION.monsterZone,[Signal.BattleFinish])

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 1

    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal:Signal.BattleFinish):
        if isSignal(signal,Signal.BattleFinish) and signal.attackerCard==self.owner:
            pass
        else:
            return False

        if signal.isDirectAttack:
            return False

        if justCheck:
            return True

        self.owner.attackCntThisTurn-=1
        if self.owner.attackCntThisTurn<0:
            self.owner.attackCntThisTurn=0
        return True


#1T:<魔法卡发动完成时>:此卡{ATK}+500{UTIL}
class MagicAddAtk(Effect):
    effType = EFF_TYPE.trigger

    observeSignals = (LOCATION.monsterZone,[Signal.ActivateSpellFinish])
    def y_activate(self,justCheck:bool,signal):
        if not isSignal(signal,Signal.ActivateSpellFinish):
            return False

        if justCheck:
            return True

        yield self.y_addCardData(self.owner,500,effDuration=EFF_DURATION.utilTurnEnds)
        return True


#1P:<场上效果>:我方场上天使族以外的怪兽{ATK}-200,{DEF}-200
class OtherDownHPMax(Effect):
    effType = EFF_TYPE.permanent

    observeSignals = (LOCATION.monsterZone,[Signal.AttachMonsterZone,Signal.CardRaceChanged, Signal.DetachMonsterZone])

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 1

    def y_signal(self, signal):
        if isSignal(signal,Signal.AttachMonsterZone) or isSignal(signal,Signal.CardRaceChanged):
            if self.owner.isInMonsterZone():
                yield from self.y_setBuffEnabled(True)
        elif isSignal(signal,Signal.DetachMonsterZone):
            if signal.card==self.owner: #me leave
                yield from self.y_setBuffEnabled(False)
            else: #other leave
                yield self.y_removeBuffEffectSource(signal.card,self.effUniID)


    def y_setBuffEnabled(self,isEnbaled):
        monsterList=self.searchCards(LOCATION.monsterZone,self.getSide(),CARD_TYPE.monster)
        shouldAddBuffList=[]
        shouldRemoveBuffList=[]
        if isEnbaled:
            for monster in monsterList:
                if monster.race!=RACE.FAIRY:
                    shouldAddBuffList.append(monster)
                else:
                    shouldRemoveBuffList.append(monster)
        else:
            shouldRemoveBuffList=monsterList

        yield self.y_addCardData(shouldAddBuffList, -200,-200, effDuration=EFF_DURATION.fromSource,
                                 uniqueSourceID=self.effUniID)
        yield self.y_removeBuffEffectSource(shouldRemoveBuffList,self.effUniID)




#1A:<场上效果>:选场上一只怪兽{ATK}+500{UTIL}
class GainAtkThisTurn(Effect):
    effType = EFF_TYPE.active

    AI_HINT = [AI_HINT.enhance]
    EFF_POWER = 1
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        foundList=self.searchCards(LOCATION.monsterZone,-1,CARD_TYPE.monster,self)
        if not foundList:
            return False
        if justCheck:
            return True

        theCard=yield self.y_select1Card(foundList,TITLE.auto,self.getSide(),canCancel=True)
        if not theCard:
            return False

        self.saveTarget1(theCard)

        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True

        theCard=self.getLegalTarget1()
        if not theCard:
            return False

        yield self.y_addCardData(theCard,500,effDuration=EFF_DURATION.utilTurnEnds)
        return True


#1I:<手牌效果>:我方怪兽被破坏时,此卡{ATK}+100
class WhenFriendDiesGain(Effect):
    effType = EFF_TYPE.instant

    observeSignals = (LOCATION.hand,[Signal.Destroyed])

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 1
    def y_cost(self,justCheck:bool,signal:Signal.Destroyed):
        if isSignal(signal,Signal.Destroyed) and signal.card.side in self.getAllySideTuple() and signal.card.isMonster():
            pass
        else:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True
        yield self.y_addCardData(self.owner,100)
        return True




#1I:<此卡被战斗破坏时>:我方回复1000LP
class BattleDesHeal(Effect):
    effType = EFF_TYPE.instant

    observeSignals = (LOCATION.grave|LOCATION.banish,[Signal.DestroyedByBattle])

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 1

    def y_activate(self,justCheck:bool,signal):
        if isSignal(signal,Signal.DestroyedByBattle,self.owner):
            pass
        else:
            return False
        if justCheck:
            return True
        yield self.y_healPlayer(self.getSide(),1000)
        return True



#场上一只怪兽返回手牌,此卡额外召唤




"""
1I:<此卡攻击时>:此卡{ATK}+1200{UTIL}
"""
class AttackWhenAdd(Effect):
    effType = EFF_TYPE.instant

    observeSignals = (LOCATION.monsterZone,[Signal.InBattle])

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 1
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal:Signal.InBattle):
        if isSignal(signal,Signal.InBattle) and signal.attackerCard==self.owner:
            pass
        else:
            return False

        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True

        yield self.y_addCardData(self.owner,1200,effDuration=EFF_DURATION.utilTurnEnds)
        return True



"""
1P:<场上效果>:此卡{ATK}和{DEF}增加 我方手牌数×800
"""
class AtkBecomeHand(Effect):
    effType = EFF_TYPE.permanent

    observeSignals = (LOCATION.monsterZone,[Signal.AttachMonsterZone,Signal.DetachMonsterZone,Signal.EnterHand,Signal.LeaveHand])

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 1
    def y_signal(self,signal):
        if isSignal(signal,Signal.DetachMonsterZone,self.owner) and not self.owner.isMonsterOnField():
            yield self.y_removeBuffEffectSource(self.owner,self.effUniID)
            return

        #TODO 测试换边
        if self.owner.isMonsterOnField():
            handNum=len(self.game.hands[self.getSide()])
            yield self.y_addCardData(self.owner,handNum*800,effDuration=EFF_DURATION.fromSource,uniqueSourceID=self.effUniID)





"""
1I:<此卡通常召唤时>:此卡{ATK}增加祭品的{ATK}数值
"""
class atkBecome2(Effect):
    effType = EFF_TYPE.instant

    observeSignals = (LOCATION.monsterZone,[Signal.NormalSummon])

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 1
    def y_activate(self,justCheck:bool,signal:Signal.NormalSummon):
        if isSignal(signal,Signal.NormalSummon,self.owner) and len(signal.tributes) and signal.tributes[0].isMonster():
            pass
        else:
            return False

        if justCheck:
            return True

        atk=signal.tributes[0].atk
        yield self.y_addCardData(self.owner,atk)
        return True


"""
1A:<场上效果>:将场上一只怪兽变为暗属性
"""
class makeDark(Effect):
    effType = EFF_TYPE.active

    activateLocation = LOCATION.monsterZone

    AI_HINT = [AI_HINT.botDontUse]
    EFF_POWER = 1
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        fieldMonsters=self.searchCards(LOCATION.monsterZone,-1,CARD_TYPE.monster,self)
        if not fieldMonsters:
            return

        if justCheck:
            return True

        target=yield self.y_select1Card(fieldMonsters,TITLE.target)
        if target:
            self.saveTarget1(target)
            return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True

        target=self.getLegalTarget1()
        if target:
            yield self.y_changeCardData(target,newAttr=ATTR.DARK)
        return True


"""
1T:<此卡通常召唤时>:此卡此回合可以攻击2次
"""
class NormalSummonAttack2(Effect):
    effType = EFF_TYPE.trigger

    observeSignals = (LOCATION.monsterZone,[Signal.NormalSummon])

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 1
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        if isSignal(signal,Signal.NormalSummon,self.owner):
            pass
        else:
            return False

        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True

        if self.owner.attackCntLimitPerTurn<2:
            yield self.y_changeCardData(self.owner,newAttackTimes=2,effDuration=EFF_DURATION.utilTurnEnds)
        return True


"""
1P:<场上效果>:此卡每回合最多攻击3次,但不能直接攻击
"""
class ThreeAttacksCantDirect(Effect):
    effType = EFF_TYPE.permanent

    uniID1=0
    uniID2=0
    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 1
    def y_locationChange(self,oldSide,oldLocation,newSide,newLocation):
        if not self.uniID1:
            self.uniID1=self.game.genUniID()
        if not self.uniID2:
            self.uniID2=self.game.genUniID()

        if newLocation==LOCATION.monsterZone:
            yield self.y_changeCardData(self.owner,newAttackTimes=3,effDuration=EFF_DURATION.fromSource,uniqueSourceID=self.uniID1)
            yield self.y_addCardBuff(self.owner,CARD_BUFF.cantDirectAttack,effDuration=EFF_DURATION.fromSource,uniqueSourceID=self.uniID2)
        else:
            yield self.y_removeBuffEffectSource(self.owner,self.uniID1)
            yield self.y_removeBuffEffectSource(self.owner,self.uniID2)


"""
1OT:<此卡攻击后>:变为守备表示并抽1张卡
"""
class AttackThenDefendAndDraw(Effect):
    effType = EFF_TYPE.optionalTrigger

    observeSignals = (LOCATION.monsterZone,[Signal.BattleFinish])

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 1
    def y_signal(self,signal):
        pass


    def y_activate(self,justCheck:bool,signal:Signal.BattleFinish):
        if isSignal(signal,Signal.BattleFinish) and signal.attackerCard==self.owner and self.owner.isMonsterOnField() and self.owner.form==FORM.attack:
            pass
        else:
            return

        if justCheck:
            return True

        yield self.y_changeForm(self.owner, FORM.defence)
        if self.owner.form==FORM.defence:
            yield self.y_drawCard(self.getSide())
        return True



"""
CardName: FireBlade
卡名: 烈焰之刃
"""

class FireBlade(Card):
    AUTHOR = "Unnamed"
    def effectsInit(self):
        self.initEffect(Equip)
        self.initEffect(FireBlade_AtkBoost)     # 装备时给目标 +800 atk

    def equipCardFilter(self,card:Card):
        return card.attr==ATTR.FIRE

"""
1A:可装备给炎属性怪兽
1P:装备怪兽{ATK}+800
"""
class Equip(Effect):
    effType = EFF_TYPE.active
    activateLocation = LOCATION.hand   # 从手牌发动

    def y_cost(self, justCheck, signal):
        if justCheck:
            maxFound=1
        else:
            maxFound=999999
        targets = self.searchCards(
            LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster,
            self, self.owner.equipCardFilter,maxFound
        )
        if not targets:
            return False

        if justCheck:
            return True

        target = yield self.y_select1Card(targets, TITLE.equip, canCancel=True)
        if not target:
            return False
        self.saveTarget1(target)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True

        target = self.getLegalTarget1()
        if not target:
            return False
        # 装备卡(self.owner)从手牌移到魔陷区,绑定到 target
        yield self.y_moveCardToSpellZone(self.owner, self.getSide(), equipToMonster=target)
        return True


"""
1P:<场上效果>:装备的怪兽{ATK}+800
"""
class FireBlade_AtkBoost(Effect):
    effType = EFF_TYPE.permanent

    observeSignals = (LOCATION.spellTrapZone, [
        Signal.EquipTo,            # 装备完成
        Signal.EquipCancel,        # 装备解除
    ])

    def y_signal(self, signal):
        if isSignal(signal, Signal.EquipCancel) and signal.equipSpell==self.owner:
            target = signal.monsterCard
            if target:
                yield self.y_removeBuffEffectSource(target, self.effUniID)
            return

        if isSignal(signal,Signal.EquipTo) and signal.equipSpell==self.owner:
            target = signal.monsterCard
            if target:
                yield self.y_addCardData(
                    target,
                    attackAdd=800,
                    effDuration=EFF_DURATION.fromSource,
                    uniqueSourceID=self.effUniID,
                )


# ============================================================
# 新增效果实现
# ============================================================

"""
1T:<场上效果>:每回合结束时,回复LP 200
"""
class TurnEndHeal200(Effect):
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone,[Signal.TurnEnds])
    AI_HINT = [AI_HINT.enhance]
    EFF_POWER = 1

    def y_cost(self,justCheck:bool,signal):
        if not isSignal(signal,Signal.TurnEnds):
            return False
        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True
        yield self.y_healPlayer(self.getSide(),200)
        return True


"""
1A:<场上效果>[从手牌丢弃1张卡]:我方场上所有怪兽本回合{ATK}+500{UTIL}
"""
class DiscardAllAtkUp500(Effect):
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.addAtk]
    EFF_POWER = 2

    def y_cost(self,justCheck:bool,signal):
        myHand=self.searchCards(LOCATION.hand,self.getSide(),CARD_TYPE.all,self)
        if not myHand:
            return False
        myMonsters=self.searchCards(LOCATION.monsterZone,self.getSide(),CARD_TYPE.monster,self)
        if not myMonsters:
            return False
        if justCheck:
            return True
        target=yield self.y_select1Card(myHand,TITLE.sendToGrave,self.getSide(),canCancel=True)
        if not target:
            return False
        yield self.y_sendCardToGrave(target)
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True
        myMonsters=self.searchCards(LOCATION.monsterZone,self.getSide(),CARD_TYPE.monster,self)
        if myMonsters:
            yield self.y_addCardData(myMonsters,attackAdd=500,
                                     effDuration=EFF_DURATION.utilTurnEnds,
                                     uniqueSourceID=self.effUniID)
        return True


"""
1P:<场上效果>:我方所有与此卡同种族的怪兽{ATK}+300
"""
class SameRaceAtkUp300(Effect):
    effType = EFF_TYPE.permanent
    observeSignals = (LOCATION.monsterZone,[
        Signal.AttachMonsterZone,
        Signal.DetachMonsterZone,
        Signal.CardRaceChanged,
    ])
    AI_HINT = [AI_HINT.permanent,AI_HINT.addAtk]
    EFF_POWER = 2

    def y_signal(self,signal):
        if isSignal(signal,Signal.DetachMonsterZone,self.owner):
            allCards=self.searchCards(LOCATION.mask_all,-1,CARD_TYPE.all,None)
            yield self.y_removeBuffEffectSource(allCards,self.effUniID)
            return

        if isSignal(signal,Signal.DetachMonsterZone):
            yield self.y_removeBuffEffectSource(signal.card,self.effUniID)
            return

        if not self.owner.isMonsterOnField():
            return

        myRace=self.owner.race
        def f(c):
            return c.race==myRace
        targets=self.searchCards(LOCATION.monsterZone,self.getSide(),CARD_TYPE.monster,None,f)
        if not targets:
            return
        yield self.y_addCardData(targets,attackAdd=300,
                                 effDuration=EFF_DURATION.fromSource,
                                 uniqueSourceID=self.effUniID)


"""
1OT:<场上效果>[不限次数]:此卡与对方怪兽进行战斗时,本次战斗中此卡{DEF}+1000
"""
class InBattleSelfDef1000(Effect):
    effType = EFF_TYPE.optionalTrigger
    observeSignals = (LOCATION.monsterZone,[Signal.InBattle])
    countLimit = COUNT_LIMIT.unlimited
    AI_HINT = [AI_HINT.enhance]
    EFF_POWER = 2

    def y_cost(self,justCheck:bool,signal:Signal.InBattle):
        if not isSignal(signal,Signal.InBattle):
            return False
        if signal.attackerCard != self.owner and signal.receiverCard != self.owner:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True
        yield self.y_addCardData(self.owner,defenceAdd=1000,
                                 effDuration=EFF_DURATION.utilBattleEnds,
                                 uniqueSourceID=self.effUniID)
        return True


"""
1A:<墓地效果>[除外此卡]:本回合我方受到的所有战斗伤害减半
"""
# 暂未实现:依赖 PLAYER_BUFF.halveBattleDamage + y_battle 内对此 buff 的减半检查
# class GraveBanishHalveBattleDamage(Effect):
#     effType = EFF_TYPE.active
#     activateLocation = LOCATION.grave
#     AI_HINT = [AI_HINT.enhance]
#     EFF_POWER = 2
#
#     def y_cost(self,justCheck:bool,signal):
#         if justCheck:
#             return True
#         yield self.y_banishCard(self.owner)
#         return True
#
#     def y_activate(self,justCheck:bool,signal):
#         if justCheck:
#             return True
#         yield self.y_addPlayerBuff(self.getSide(),PLAYER_BUFF.halveBattleDamage,
#                                    EFF_DURATION.utilTurnEnds,self.effUniID)
#         return True


"""
1T:<场上效果>[不限次数]:我方其他怪兽被破坏时,回复LP 500
"""
class OtherDestroyedHeal500(Effect):
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone,[Signal.Destroyed])
    countLimit = COUNT_LIMIT.unlimited
    AI_HINT = [AI_HINT.enhance]
    EFF_POWER = 1

    def y_cost(self,justCheck:bool,signal):
        if not isSignal(signal,Signal.Destroyed):
            return False
        if signal.card is None or signal.card is self.owner:
            return False
        if signal.card.side != self.getSide():
            return False
        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True
        yield self.y_healPlayer(self.getSide(),500)
        return True


"""
1A:<场上效果>[支付LP 1000]:抽1张卡,此卡本回合{ATK}+500{UTIL}
"""
class PayLP1000DrawAndAtkUp500(Effect):
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.drawCard,AI_HINT.addAtk]
    EFF_POWER = 3

    def y_cost(self,justCheck:bool,signal):
        myLP=self.game.LPs[self.getSide()]
        if myLP<=1000:
            return False
        deckCards=self.game.decks[self.getSide()]
        if not deckCards:
            return False
        if justCheck:
            return True
        self.game.damagePlayer(self.getSide(),1000,False)
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True
        yield self.y_drawCard(self.getSide())
        if self.owner.isMonsterOnField():
            yield self.y_addCardData(self.owner,attackAdd=500,
                                     effDuration=EFF_DURATION.utilTurnEnds,
                                     uniqueSourceID=self.effUniID)
        return True


"""
1P:<场上效果>:我方场上每有1只其他怪兽,此卡{ATK}+200
"""
class PerOtherMonsterAtk200(Effect):
    effType = EFF_TYPE.permanent
    observeSignals = (LOCATION.monsterZone,[
        Signal.AttachMonsterZone,
        Signal.DetachMonsterZone,
    ])
    AI_HINT = [AI_HINT.permanent,AI_HINT.addAtk]
    EFF_POWER = 2

    def y_signal(self,signal):
        if isSignal(signal,Signal.DetachMonsterZone,self.owner):
            yield self.y_removeBuffEffectSource(self.owner,self.effUniID)
            return

        if not self.owner.isMonsterOnField():
            return

        others=self.searchCards(LOCATION.monsterZone,self.getSide(),CARD_TYPE.monster,None,
                                lambda c:c is not self.owner)
        # 先清旧 buff,再按当前其他怪兽数加新 buff
        yield self.y_removeBuffEffectSource(self.owner,self.effUniID)
        if others:
            yield self.y_addCardData(self.owner,attackAdd=200*len(others),
                                     effDuration=EFF_DURATION.fromSource,
                                     uniqueSourceID=self.effUniID)


"""
1OT:<场上效果>[不限次数]:此卡宣言攻击时,本次战斗中此卡{ATK}变为对方怪兽{ATK}+100{UTIL}
"""
class DeclareAttackAtkBecomeEnemyPlus100(Effect):
    effType = EFF_TYPE.optionalTrigger
    observeSignals = (LOCATION.monsterZone,[Signal.RequestBattle])
    countLimit = COUNT_LIMIT.unlimited
    AI_HINT = [AI_HINT.addAtk]
    EFF_POWER = 2

    def y_cost(self,justCheck:bool,signal:Signal.RequestBattle):
        if not isSignal(signal,Signal.RequestBattle):
            return False
        if signal.attackerCard != self.owner:
            return False
        if signal.receiverCard is None:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal:Signal.RequestBattle):
        if justCheck:
            return True
        newAtk=signal.receiverCard.atk+100
        yield self.y_changeCardData(self.owner,newAtk=newAtk,
                                    effDuration=EFF_DURATION.utilBattleEnds,
                                    uniqueSourceID=self.effUniID)
        return True


"""
1A:<手牌效果>[除外此卡]:我方场上1只怪兽本回合{ATK}+1000{UTIL}
"""
class HandBanishOneAtkUp1000(Effect):
    effType = EFF_TYPE.active
    activateLocation = LOCATION.hand
    AI_HINT = [AI_HINT.addAtk]
    EFF_POWER = 2

    def y_cost(self,justCheck:bool,signal):
        myMonsters=self.searchCards(LOCATION.monsterZone,self.getSide(),CARD_TYPE.monster,self)
        if not myMonsters:
            return False
        if justCheck:
            return True
        target=yield self.y_select1Card(myMonsters,TITLE.target,self.getSide(),canCancel=True)
        if not target:
            return False
        yield self.y_banishCard(self.owner)
        self.saveTarget1(target)
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True
        target=self.getLegalTarget1()
        if target:
            yield self.y_addCardData(target,attackAdd=1000,
                                     effDuration=EFF_DURATION.utilTurnEnds,
                                     uniqueSourceID=self.effUniID)
        return True
