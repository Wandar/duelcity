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
[Send 1 card from your hand to the Graveyard]:Change the form of 1 monster on your opponent's field.

"""


"""
陷阱卡

[对方怪兽攻击时发动]:攻击怪兽-2点攻击力直到回合结束

"""


"""
1A:[献祭此卡]:对对方场上所有怪兽造成200点伤害
"""
class TributeDamage(Effect):
    effType = EFF_TYPE.active

    activateLocation = LOCATION.monsterZone

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 1
    def y_cost(self,justCheck:bool,signal):
        if justCheck:
            return True
        successNum=yield self.y_tributeCard(self.owner)
        return successNum!=0

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True

        enemyMonsters=self.searchCards(LOCATION.monsterZone,self.getEnemySideTuple(),CARD_TYPE.monster,self)
        yield self.y_damageCard(enemyMonsters,200)
        return True



"""
1OT:<此卡召唤时>:对对方场上一只怪兽造成1点伤害
"""
class SummonDamage(Effect):
    effType = EFF_TYPE.optionalTrigger

    observeSignals = (LOCATION.monsterZone,[Signal.Summon])

    AI_HINT = [AI_HINT.damager]
    EFF_POWER = 1
    def y_cost(self,justCheck:bool,signal):
        if isSignal(signal,Signal.Summon,self.owner):
            pass
        else:
            return False

        enMonsters=self.searchCards(LOCATION.monsterZone,self.getEnemySideTuple(),CARD_TYPE.monster,self)
        if not enMonsters:
            return False

        if justCheck:
            return True

        en=yield self.y_select1Card(enMonsters,TITLE.damage,canCancel=True)
        if not en:
            return False
        self.saveTarget1(en)
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True

        en=self.getLegalTarget1()
        yield self.y_damageCard(en,1)
        return True



#1I:<对方召唤怪兽时>:对该怪兽造成300点伤害
class SummonBeDamaged(Effect):
    effType = EFF_TYPE.instant

    observeSignals = (LOCATION.monsterZone,[Signal.Summon])

    AI_HINT = [AI_HINT.blockNewMonster]

    def y_activate(self,justCheck:bool,signal):
        if isSignal(signal,Signal.Summon) and signal.card.side!=self.getSide() and signal.card.isMonsterOnField():
            pass
        else:
            return False

        if justCheck:
            return True

        yield self.y_damageCard(signal.card,300)
        return True




#1A:[献祭此卡]:获得对方场上所有LV3以下怪兽的控制权
class allDamageSpell(Effect):
    effType = EFF_TYPE.active

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 1

    def y_activate(self,justCheck:bool,signal):
        allMonsters=self.searchCards(LOCATION.monsterZone,-1,CARD_TYPE.monster,self)

        if not allMonsters:
            return False

        if justCheck:
            return True

        yield self.y_damageCard(allMonsters,100)
        return True

#1A:破坏对方场上HP最低的一只怪兽(多只时随机)
"""
1T:<此卡召唤时>:对对方造成500点伤害
"""
class SummonDamagePlayer(Effect):
    effType = EFF_TYPE.trigger

    observeSignals = (LOCATION.monsterZone,[Signal.Summon])

    AI_HINT = [AI_HINT.eraser]
    AI_POWER = 1
    def y_signal(self,signal):
        pass

    enemySide=0
    def y_cost(self,justCheck:bool,signal):
        if isSignal(signal,Signal.Summon,self.owner):
            pass
        else:
            return
        if justCheck:
            return True

        self.enemySide=yield self.y_select1EnemySide()
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True

        yield self.y_damagePlayer(self.enemySide,500)
        return True

"""
1T:<被战斗破坏时>:破坏对方场上一张魔法·陷阱卡
"""
class DestroyedByBattleDestroyMagic(Effect):
    effType = EFF_TYPE.trigger

    observeSignals = (LOCATION.grave,[Signal.DestroyedByBattle])

    AI_HINT = [AI_HINT.eraser]
    AI_POWER = 1
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal:Signal.DestroyedByBattle):
        if isSignal(signal,Signal.DestroyedByBattle,self.owner):
            pass
        else:
            return

        enemyMagicTrap=self.searchCards(LOCATION.spellTrapZone,self.getEnemySideTuple(),CARD_TYPE.all,self)
        if not enemyMagicTrap:
            return

        if justCheck:
            return True

        card=yield self.y_select1Card(enemyMagicTrap,TITLE.destroy)
        self.saveTarget1(card)
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True

        target=self.getLegalTarget1()
        if target:
            yield self.y_destroyCard(target)
        return True

# ============================================================
# 新增效果实现
# ============================================================

"""
1OT:此卡战斗破坏对方怪兽时,对对方造成被破坏怪兽{ATK}一半的伤害
"""
class BattleDestroyDamageHalfAtk(Effect):
    effType = EFF_TYPE.optionalTrigger
    observeSignals = (LOCATION.monsterZone,[Signal.BattleFinish])
    AI_HINT = [AI_HINT.damager]
    EFF_POWER = 2

    def y_cost(self,justCheck:bool,signal:Signal.BattleFinish):
        if not isSignal(signal,Signal.BattleFinish):
            return False
        if signal.attackerCard != self.owner:
            return False
        if signal.receiverCard is None:
            return False
        if signal.receiverCard.isMonsterOnField():
            return False
        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal:Signal.BattleFinish):
        if justCheck:
            return True
        damageAmount=signal.receiverCard.atk_0//2
        if damageAmount>0:
            yield self.y_damagePlayer(self.getEnemySideTuple(),damageAmount)
        return True


"""
1A:[解放此卡]:对对方场上所有怪兽的控制者各造成500伤害
"""
class TributeDamageEachEnemyMonster(Effect):
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.damager]
    EFF_POWER = 2

    def y_cost(self,justCheck:bool,signal):
        enemyMonsters=self.searchCards(LOCATION.monsterZone,self.getEnemySideTuple(),CARD_TYPE.monster,self)
        if not enemyMonsters:
            return False
        if justCheck:
            return True
        successNum=yield self.y_tributeCard(self.owner)
        return successNum!=0

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True
        enemyMonsters=self.searchCards(LOCATION.monsterZone,self.getEnemySideTuple(),CARD_TYPE.monster,self)
        if not enemyMonsters:
            return False
        sideToCount={}
        for c in enemyMonsters:
            sideToCount[c.side]=sideToCount.get(c.side,0)+1
        for side,count in sideToCount.items():
            yield self.y_damagePlayer(side,500*count)
        return True


"""
1T:<此卡被破坏送去墓地时>:对对方造成1000伤害
"""
class DestroyedDamage1000(Effect):
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.grave,[Signal.Destroyed])
    AI_HINT = [AI_HINT.damager]
    EFF_POWER = 2

    def y_cost(self,justCheck:bool,signal):
        if not isSignal(signal,Signal.Destroyed,self.owner):
            return False
        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True
        yield self.y_damagePlayer(self.getEnemySideTuple(),1000)
        return True


"""
1T:[不限次数]:对方每次发动魔法卡时,对对方造成300伤害
"""
class OppActivateSpellDamage300(Effect):
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone,[Signal.BeforeActivateEffect])
    countLimit = COUNT_LIMIT.unlimited
    AI_HINT = [AI_HINT.damager]
    EFF_POWER = 2

    def y_cost(self,justCheck:bool,signal:Signal.BeforeActivateEffect):
        if not isSignal(signal,Signal.BeforeActivateEffect):
            return False
        if signal.cardType&CARD_TYPE.spell==0:
            return False
        if signal.effect is None:
            return False
        if signal.effect.getSide()==self.getSide():
            return False
        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True
        yield self.y_damagePlayer(self.getEnemySideTuple(),300)
        return True


"""
1OT:[不限次数]:我方抽卡时,对对方造成200伤害
"""
class MyDrawDamage200(Effect):
    effType = EFF_TYPE.optionalTrigger
    observeSignals = (LOCATION.monsterZone,[Signal.DrawCard])
    countLimit = COUNT_LIMIT.unlimited
    AI_HINT = [AI_HINT.damager]
    EFF_POWER = 1

    def y_cost(self,justCheck:bool,signal:Signal.DrawCard):
        if not isSignal(signal,Signal.DrawCard):
            return False
        if not signal.cardList:
            return False
        if signal.cardList[0].side!=self.getSide():
            return False
        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True
        yield self.y_damagePlayer(self.getEnemySideTuple(),200)
        return True


"""
1A:[从手牌丢弃2张卡]:对对方造成2000伤害
"""
class Discard2Damage2000(Effect):
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.damager]
    EFF_POWER = 3

    def y_cost(self,justCheck:bool,signal):
        myHand=self.searchCards(LOCATION.hand,self.getSide(),CARD_TYPE.all,self)
        if len(myHand)<2:
            return False
        if justCheck:
            return True
        c1=yield self.y_select1Card(myHand,TITLE.sendToGrave,self.getSide(),canCancel=True)
        if not c1:
            return False
        yield self.y_sendCardToGrave(c1)
        myHand=self.searchCards(LOCATION.hand,self.getSide(),CARD_TYPE.all,self)
        if not myHand:
            return False
        c2=yield self.y_select1Card(myHand,TITLE.sendToGrave,self.getSide(),canCancel=True)
        if not c2:
            return False
        yield self.y_sendCardToGrave(c2)
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True
        yield self.y_damagePlayer(self.getEnemySideTuple(),2000)
        return True


"""
1T:对方回合结束时,若此卡本回合未宣言攻击,对对方造成500伤害
"""
class OppTurnEndNoAttackDamage500(Effect):
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone,[Signal.TurnEnds])
    AI_HINT = [AI_HINT.damager]
    EFF_POWER = 1

    def y_cost(self,justCheck:bool,signal):
        if not isSignal(signal,Signal.TurnEnds):
            return False
        if self.game.whoseTurn==self.getSide():
            return False
        if self.owner.attackCntThisTurn!=0:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True
        yield self.y_damagePlayer(self.getEnemySideTuple(),500)
        return True


"""
1A:<墓地效果>[除外此卡和墓地其他1只怪兽]:对对方造成1500伤害
"""
class GraveBanishSelfPlusOneDamage1500(Effect):
    effType = EFF_TYPE.active
    activateLocation = LOCATION.grave
    AI_HINT = [AI_HINT.damager]
    EFF_POWER = 3

    def y_cost(self,justCheck:bool,signal):
        myGraveOthers=self.searchCards(LOCATION.grave,self.getSide(),CARD_TYPE.monster,self,
                                       lambda c:c is not self.owner)
        if not myGraveOthers:
            return False
        if justCheck:
            return True
        target=yield self.y_select1Card(myGraveOthers,TITLE.banish,self.getSide(),canCancel=True)
        if not target:
            return False
        yield self.y_banishCard(self.owner)
        yield self.y_banishCard(target)
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True
        yield self.y_damagePlayer(self.getEnemySideTuple(),1500)
        return True


"""
1T:<此卡被战斗破坏时>:对破坏此卡的怪兽控制者造成此卡原{ATK}的伤害
"""
class BattleDestroyedSelfDamageEqualAtk(Effect):
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.grave,[Signal.DestroyedByBattle])
    AI_HINT = [AI_HINT.damager]
    EFF_POWER = 2

    def y_cost(self,justCheck:bool,signal:Signal.DestroyedByBattle):
        if not isSignal(signal,Signal.DestroyedByBattle,self.owner):
            return False
        if signal.reasonCard is None:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal:Signal.DestroyedByBattle):
        if justCheck:
            return True
        damageAmount=self.owner.atk_0
        if damageAmount>0:
            yield self.y_damagePlayer(signal.reasonCard.side,damageAmount)
        return True


"""
1A:[支付LP 500]:对我方或对方1只怪兽造成800伤害
"""
class PayLP500DamageMonster800(Effect):
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.damager]
    EFF_POWER = 2

    def y_cost(self,justCheck:bool,signal):
        myLP=self.game.LPs[self.getSide()]
        if myLP<=500:
            return False
        allMonsters=self.searchCards(LOCATION.monsterZone,-1,CARD_TYPE.monster,self)
        if not allMonsters:
            return False
        if justCheck:
            return True
        target=yield self.y_select1Card(allMonsters,TITLE.damage,self.getSide(),canCancel=True)
        if not target:
            return False
        self.game.damagePlayer(self.getSide(),500,False)
        self.saveTarget1(target)
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True
        target=self.getLegalTarget1()
        if target:
            yield self.y_damageCard(target,800)
        return True
