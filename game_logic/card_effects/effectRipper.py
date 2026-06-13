# -*- coding: utf-8 -*-
from __future__ import annotations
from annos import *
from KBEDebug import *
from a import Signal, fitter
from b.Card import *
from a.Effect import *
from a.DuelConstants import *
from Constants import *
import random


"""
[Send 1 card from your hand to the Graveyard]:Change the form of 1 monster on your opponent's field.

"""


"""
陷阱卡

[对方怪兽攻击时发动]:攻击怪兽-2点攻击力直到回合结束

"""


"""
1OI:<对方召唤怪兽时>[献祭一只我方怪兽]:破坏该怪兽
"""
class summon_negative(Effect):
    effType = EFF_TYPE.optionalInstant

    observeSignals = (LOCATION.spellTrapZone,[Signal.Summon])

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 1
    def y_cost(self,justCheck:bool,signal:Signal.Summon):
        if isSignal(signal,Signal.Summon) and signal.card.side in self.getEnemySideTuple():
            pass
        else:
            return False

        selfmonsters=self.searchCards(LOCATION.monsterZone,self.getSide(),CARD_TYPE.monster)
        if not selfmonsters:
            return False
        if justCheck:
            return True

        themonster=yield self.y_select1Card(selfmonsters,TITLE.tribute,self.getSide(),canCancel=True)
        if not themonster:
            return False
        yield self.y_tributeCard(themonster)
        return True

    def y_activate(self,justCheck:bool,signal:Signal.Summon):
        if justCheck:
            return True

        yield self.y_destroyCard(signal.card)
        return True


class TributeAndControl(Effect):
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
        def f(card):
            return card.level<=3
        enemyMonsters=self.searchCards(LOCATION.monsterZone,self.getEnemySideTuple(),CARD_TYPE.monster,self,f)
        if not enemyMonsters:
            return False
        if justCheck:
            return True

        tributeNum=yield self.y_tributeCard(self.owner)
        if not tributeNum:
            return False
        yield self.y_changeMonsterController(enemyMonsters,self.getSide())
        return True


#1A:[献祭此卡]:破坏场上一只怪兽
class TributeSelfDestroy(Effect):
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 1

    def y_activate(self,justCheck:bool,signal):
        monstersOnField=self.searchCards(LOCATION.monsterZone,-1)
        if len(monstersOnField)<2:
            return False

        if justCheck:
            return True

        tributeNum=yield self.y_tributeCard(self.owner)
        if not tributeNum:
            return False

        monstersOnField=self.searchCards(LOCATION.monsterZone,-1)
        if not monstersOnField:
            return False
        card=yield self.y_select1Card(monstersOnField,TITLE.destroy,self.getSide())
        yield self.y_destroyCard(card)
        return True



#1A:[献祭我方场上一只怪兽]:破坏对方场上一只HP不大于祭品HP的怪兽
class TributeDestroy(Effect):
    effType = EFF_TYPE.active

    AI_HINT = [AI_HINT.highCost,AI_HINT.eraser]
    EFF_POWER = 1
    def y_cost(self,justCheck:bool,signal):
        enemyMonsters=self.searchCards(LOCATION.monsterZone,self.getEnemySideTuple(),CARD_TYPE.monster,self)
        if not enemyMonsters:
            return False
        monsters=self.searchCards(LOCATION.monsterZone,self.getSide(),CARD_TYPE.monster,self)
        if not monsters:
            return False

        if justCheck:
            return True

        thecard=yield self.y_select1Card(monsters,TITLE.tribute,self.getSide(),canCancel=False)
        if not thecard:
            return False

        thecardHP=thecard.hp
        tributeNum=yield self.y_tributeCard(thecard)
        if not tributeNum:
            return False

        def filterDestroy(card):
            if card.hp<=thecardHP:
                return True
            return False

        monsters=self.searchCards(LOCATION.monsterZone,self.getEnemySideTuple(),CARD_TYPE.monster,self,filterDestroy)
        destroyMonster=yield self.y_select1Card(monsters,TITLE.destroy,self.getSide(),canCancel=False)
        if not destroyMonster:
            return False
        self.saveTarget1(destroyMonster)

        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True

        destroyMonster=self.getLegalTarget1()
        if not destroyMonster:
            return False
        yield self.y_destroyCard(destroyMonster)
        return True





#1A:对场上所有怪兽造成100点伤害
class destroyLowestHP_effect1(Effect):
    effType = EFF_TYPE.active


    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 1
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal):
        enemyMonsters=self.searchCards(LOCATION.monsterZone,self.getEnemySideTuple(),CARD_TYPE.monster)
        if not enemyMonsters:
            return False
        if justCheck:
            return True

        lowestHP=1000000
        for card in enemyMonsters:
            if card.hp<lowestHP:
                lowestHP=card.hp

        cardList=[]
        for card in enemyMonsters:
            if card.hp==lowestHP:
                cardList.append(card)

        thecard=random.choice(cardList)
        yield self.y_destroyCard(thecard)
        return True

"""
1OT:<通常召唤后>:将对方场上一张卡返回手牌
"""
class normalSummonWind(Effect):
    effType = EFF_TYPE.optionalTrigger

    observeSignals = (LOCATION.monsterZone,[Signal.NormalSummon])

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 1

    def y_activate(self,justCheck:bool,signal):
        if isSignal(signal,Signal.NormalSummon,self.owner):
            pass
        else:
            return False

        enemyCards=self.searchCards(LOCATION.mask_onField,self.getEnemySideTuple(),affectSource=self)

        if not enemyCards:
            return False
        if justCheck:
            return True

        thecard=yield self.y_select1Card(enemyCards,TITLE.returnToHand)
        if thecard:
            yield self.y_returnCardToHand(thecard)

        return True


"""
1A:[丢弃一张手牌]:破坏对方场上所有与丢弃的牌相同卡种的卡
"""
class dropHandCardDestroy(Effect):
    effType = EFF_TYPE.active

    activateLocation = LOCATION.monsterZone

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 1

    thecardType=0

    def y_cost(self,justCheck:bool,signal):
        handcards=self.game.hands[self.getSide()]
        if not handcards:
            return False

        if justCheck:
            return True

        thetarget=yield self.y_select1Card(handcards,TITLE.sendToGrave,canCancel=True) #type:Card
        if thetarget:
            successNum=yield self.y_sendCardToGrave(thetarget)
            if successNum:
                self.thecardType=thetarget.getBasicCardType()
                return True
        return False

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True
        if self.thecardType:
            enemyCards=self.searchCards(LOCATION.mask_onField,self.getEnemySideTuple(),self.thecardType,self)
            yield self.y_destroyCard(enemyCards)

        return True


"""
1I:<战斗效果>:此卡与战斗对象都返回手牌
"""
class BattleReturnHand(Effect):
    effType = EFF_TYPE.instant

    observeSignals = (LOCATION.monsterZone,[Signal.InBattle])

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 1
    def y_signal(self,signal):
        pass

    def y_activate(self,justCheck:bool,signal:Signal.InBattle):
        if signal.battleType==BATTLE_TYPE.directAttack:
            return False
        if signal.attackerCard==self.owner or signal.receiverCard==self.owner:
            pass
        else:
            return False

        if justCheck:
            return True

        l=[c for c in (signal.attackerCard,signal.receiverCard) if c]
        yield self.y_returnCardToHand(l)

        return True



"""
1OT:<通常召唤后>:将场上一张卡返回其持有者卡组顶端
"""
class normalSummonReturnToDeckTop(Effect):
    effType = EFF_TYPE.optionalTrigger

    observeSignals = (LOCATION.monsterZone,[Signal.NormalSummon])

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 1
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal:Signal.NormalSummon):
        if isSignal(signal,Signal.NormalSummon,self.owner):
            pass
        else:
            return False

        fieldCards=self.searchCards(LOCATION.mask_onField,-1,affectSource=self)
        if not fieldCards:
            return False

        if justCheck:
            return True

        target=yield self.y_select1Card(fieldCards,TITLE.returnToDeck,canCancel=True)
        if target:
            self.saveTarget1(target)

            return True
        return False

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True

        target=self.getLegalTarget1()
        if target:
            yield self.y_returnCardToDeck(target,RETURN_TO_DECK.top)
        return True



"""
1T:<此卡表示形式改变时>:改变对方一只怪兽的表示形式
"""
class EffChangePosition(Effect):
    effType = EFF_TYPE.trigger

    observeSignals = (LOCATION.monsterZone,[Signal.CardChangeForm])

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 1

    def y_cost(self,justCheck:bool,signal:Signal.CardChangeForm):
        if isSignal(signal,Signal.CardChangeForm,self.owner):
            pass
        else:
            return False

        enemyMonsters=self.searchCards(LOCATION.monsterZone,self.getEnemySideTuple(),CARD_TYPE.monster,self)

        if not enemyMonsters:
            return False

        if justCheck:
            return True

        thetarget=yield self.y_select1Card(enemyMonsters,TITLE.changeForm,canCancel=False)
        if thetarget:
            self.saveTarget1(thetarget)
            return True
        return False

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True

        thetarget=self.getLegalTarget1()
        if thetarget:
            yield self.y_changeForm(thetarget)
        return True



"""
1T:<被破坏后>:除外对方场上一张卡
"""
class paohulong_effect2(Effect):
    effType = EFF_TYPE.trigger

    observeSignals = (LOCATION.mask_all,[Signal.Destroyed])

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 1
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal:Signal.Destroyed):
        if isSignal(signal,Signal.Destroyed) and signal.card==self.owner:
            pass
        else:
            return False

        enemyCards=self.searchCards(LOCATION.mask_onField,self.getEnemySideTuple(),CARD_TYPE.all,self)

        if not enemyCards:
            return False

        if justCheck:
            return True

        theTarget=yield self.y_select1Card(enemyCards,TITLE.banish)
        self.saveTarget1(theTarget)
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True

        target=self.getLegalTarget1()
        if target:
            yield self.y_banishCard(target)
        return True

"""
1T:<被献祭后>:对方场上一只怪兽{ATK}-500
"""
class TributeDownAtk(Effect):
    effType = EFF_TYPE.trigger

    observeSignals = (LOCATION.monsterZone,[Signal.Tributed])

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 1
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        if isSignal(signal,Signal.Tributed,self.owner):
            pass
        else:
            return

        enemyMonsters=self.searchCards(LOCATION.monsterZone,self.getEnemySideTuple(),CARD_TYPE.monster,self)

        if not enemyMonsters:
            return

        if justCheck:
            return True

        target=yield self.y_select1Card(enemyMonsters,TITLE.specialSummon ,canCancel=True)
        if target:
            self.saveTarget1(target)
            return True

        return

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True

        target=self.getLegalTarget1()
        if target:
            yield self.y_addCardData(target,-500)



"""
1OI:<通常召唤后>:破坏场上一张魔法·陷阱卡
"""
class NormalSummonDestroyMagic(Effect):
    effType = EFF_TYPE.optionalInstant

    observeSignals = (LOCATION.monsterZone,[Signal.NormalSummon])

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 1
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal:Signal.NormalSummon):
        if isSignal(signal,Signal.NormalSummon,self.owner):
            pass
        else:
            return

        magicTraps=self.searchCards(LOCATION.spellTrapZone,affectSource=self)

        if not magicTraps:
            return
        if justCheck:
            return True

        target=yield self.y_select1Card(magicTraps,TITLE.destroy)
        if not target:
            return

        self.saveTarget1(target)

        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True

        target=self.getLegalTarget1()
        if not target:
            return

        yield self.y_destroyCard(target)
        return True

"""
1A:将对方一只怪兽变为守备表示
"""
class MakeMonsterDefend(Effect):
    effType = EFF_TYPE.active

    activateLocation = LOCATION.monsterZone

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 1
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        enemyMonsters=self.searchCards(LOCATION.monsterZone,self.getEnemySideTuple(),CARD_TYPE.monster,self)
        if not enemyMonsters:
            return
        if justCheck:
            return True

        target=yield self.y_select1Card(enemyMonsters,TITLE.changeForm)
        if not target:
            return
        self.saveTarget1(target)
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True

        target=self.getLegalTarget1()
        if target:
            yield self.y_changeForm(target, FORM.defence)
        return True


"""
1A:破坏对方场上一只{ATK}低于此卡的怪兽
"""
class DestroyAtkLowMonster(Effect):
    effType = EFF_TYPE.active

    activateLocation = LOCATION.monsterZone

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 1
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        selfatk=self.owner.atk
        def f(card):
            if card.atk<selfatk:
                return True
        enemyMonsters=self.searchCards(LOCATION.monsterZone,self.getEnemySideTuple(),CARD_TYPE.monster,self,filterFunc=f)
        if not enemyMonsters:
            return

        if justCheck:
            return True

        target=yield self.y_select1Card(enemyMonsters,TITLE.destroy)
        if not target:
            return
        self.saveTarget1(target)
        return True

    def y_activate(self,justCheck:bool,signal):

        if justCheck:
            return True

        target=self.getLegalTarget1()
        if target:
            if target.atk>=self.owner.atk:
                return
            yield self.y_destroyCard(target)
        return True


"""
1A:我方墓地有5只以上怪兽时,破坏对方场上{DEF}最低的一只怪兽
"""
class DestroyGraveOver5(Effect):
    effType = EFF_TYPE.active

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 1
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        myGraveMonsters=self.searchCards(LOCATION.grave,self.getSide(),CARD_TYPE.monster)
        if len(myGraveMonsters)<5:
            return

        enemyMonsters=self.searchCards(LOCATION.monsterZone,self.getEnemySideTuple(),CARD_TYPE.monster,self)
        if not enemyMonsters:
            return
        min_def = min(card.defence for card in enemyMonsters)
        weakest = [card for card in enemyMonsters if card.defence == min_def]

        if justCheck:
            return True

        if len(weakest)==1:
            target=weakest[0]
        else:
            target=yield self.y_select1Card(weakest,TITLE.destroy)
        self.saveTarget1(target)
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True
        target=self.getLegalTarget1()
        if target:
            yield self.y_destroyCard(target)
        return True


"""
1A:[将手牌中1只怪兽送去墓地]:除外对方场上一只与被送去墓地的怪兽相同属性的怪兽
"""
class SameAttrBanish(Effect):
    effType = EFF_TYPE.active


    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 1

    theAttr=ATTR.none
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        handMonsters=self.searchCards(LOCATION.hand,self.getSide(),CARD_TYPE.monster)

        enemyMonster=self.searchCards(LOCATION.monsterZone,self.getEnemySideTuple(),CARD_TYPE.monster,self)
        if not handMonsters:
            return
        if not enemyMonster:
            return
        if justCheck:
            return True

        sendcard=yield self.y_select1Card(handMonsters,TITLE.sendToGrave) #type:Card
        if not sendcard:
            return
        self.theAttr=sendcard.attr
        targetList=[card for card in enemyMonster if card.attr==self.theAttr]
        if not targetList:
            return

        sendNum=yield self.y_sendCardToGrave(sendcard)
        if sendNum==0:
            return

        targetEnemyMonster=yield self.y_select1Card(targetList,TITLE.banish)
        if not targetEnemyMonster:
            return

        self.saveTarget1(targetEnemyMonster)
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True

        target=self.getLegalTarget1()
        if target.attr==self.theAttr:
            yield self.y_banishCard(target)
        return True

# ============================================================
# 新增效果实现
# ============================================================

"""
1A:[解放此卡]:将对方场上所有LV4以下怪兽返回手牌
"""
class TributeReturnAllEnemyLv4(Effect):
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 3

    def y_cost(self,justCheck:bool,signal):
        targets=self.searchCards(LOCATION.monsterZone,self.getEnemySideTuple(),CARD_TYPE.monster,
                                 self,lambda c:c.level<=4)
        if not targets:
            return False
        if justCheck:
            return True
        successNum=yield self.y_tributeCard(self.owner)
        return successNum!=0

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True
        targets=self.searchCards(LOCATION.monsterZone,self.getEnemySideTuple(),CARD_TYPE.monster,
                                 self,lambda c:c.level<=4)
        if targets:
            yield self.y_returnCardToHand(targets)
        return True


"""
1OT:<被特殊召唤时>:破坏对方场上1张魔法/陷阱卡
"""
class SpecialSummonedDestroyEnemySpell(Effect):
    effType = EFF_TYPE.optionalTrigger
    observeSignals = (LOCATION.monsterZone,[Signal.SpecialSummon])
    AI_HINT = [AI_HINT.spellDestroyer]
    EFF_POWER = 2

    def y_cost(self,justCheck:bool,signal):
        if not isSignal(signal,Signal.SpecialSummon,self.owner):
            return False
        enemySpells=self.searchCards(LOCATION.spellTrapZone,self.getEnemySideTuple(),CARD_TYPE.all,self)
        if not enemySpells:
            return False
        if justCheck:
            return True
        target=yield self.y_select1Card(enemySpells,TITLE.destroy,self.getSide(),canCancel=True)
        if not target:
            return False
        self.saveTarget1(target)
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True
        target=self.getLegalTarget1()
        if target:
            yield self.y_destroyCard(target)
        return True


"""
1A:[从手牌丢弃1张卡]:除外对方墓地1只怪兽
"""
class DiscardBanishEnemyGrave(Effect):
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 2

    def y_cost(self,justCheck:bool,signal):
        myHand=self.searchCards(LOCATION.hand,self.getSide(),CARD_TYPE.all,self)
        if not myHand:
            return False
        enemyGrave=self.searchCards(LOCATION.grave,self.getEnemySideTuple(),CARD_TYPE.monster,self)
        if not enemyGrave:
            return False
        if justCheck:
            return True
        discardCard=yield self.y_select1Card(myHand,TITLE.sendToGrave,self.getSide(),canCancel=True)
        if not discardCard:
            return False
        yield self.y_sendCardToGrave(discardCard)
        target=yield self.y_select1Card(enemyGrave,TITLE.banish,self.getSide(),canCancel=True)
        if not target:
            return False
        self.saveTarget1(target)
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True
        target=self.getLegalTarget1()
        if target:
            yield self.y_banishCard(target)
        return True


"""
1T:<此卡被战斗破坏时>:破坏战斗中的对方怪兽
"""
class BattleDestroyedDestroyEnemy(Effect):
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.grave,[Signal.DestroyedByBattle])
    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 2

    def y_cost(self,justCheck:bool,signal:Signal.DestroyedByBattle):
        if not isSignal(signal,Signal.DestroyedByBattle,self.owner):
            return False
        if signal.reasonCard is None:
            return False
        if not signal.reasonCard.isMonsterOnField():
            return False
        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal:Signal.DestroyedByBattle):
        if justCheck:
            return True
        if signal.reasonCard and signal.reasonCard.isMonsterOnField():
            yield self.y_destroyCard(signal.reasonCard)
        return True


"""
1A:将我方场上1只LV4以下怪兽返回手牌,破坏对方场上1只{ATK}最高的怪兽
"""
class ReturnLv4DestroyHighestAtk(Effect):
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 3

    def y_cost(self,justCheck:bool,signal):
        myLv4=self.searchCards(LOCATION.monsterZone,self.getSide(),CARD_TYPE.monster,self,
                               lambda c:c.level<=4)
        if not myLv4:
            return False
        enemyMonsters=self.searchCards(LOCATION.monsterZone,self.getEnemySideTuple(),CARD_TYPE.monster,self)
        if not enemyMonsters:
            return False
        if justCheck:
            return True
        target=yield self.y_select1Card(myLv4,TITLE.returnToHand,self.getSide(),canCancel=True)
        if not target:
            return False
        yield self.y_returnCardToHand(target)
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True
        enemyMonsters=self.searchCards(LOCATION.monsterZone,self.getEnemySideTuple(),CARD_TYPE.monster,self)
        if not enemyMonsters:
            return False
        maxAtk=max(c.atk for c in enemyMonsters)
        topAtkList=[c for c in enemyMonsters if c.atk==maxAtk]
        target=topAtkList[0]
        if len(topAtkList)>1:
            target=yield self.y_select1Card(topAtkList,TITLE.destroy,self.getSide(),canCancel=False)
        if target:
            yield self.y_destroyCard(target)
        return True


"""
1OI:[解放此卡]:对方发动魔法卡时,无效该魔法卡发动并破坏
"""
class TributeCounterSpell(Effect):
    effType = EFF_TYPE.optionalInstant
    observeSignals = (LOCATION.monsterZone,[Signal.BeforeActivateEffect])
    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 4

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
        srcCard=getattr(signal,'sourceCard',None) or signal.effect.owner
        self.saveTarget1(srcCard)
        successNum=yield self.y_tributeCard(self.owner)
        return successNum!=0

    def y_activate(self,justCheck:bool,signal:Signal.BeforeActivateEffect):
        if justCheck:
            return True
        yield self.y_counterEffectActivate(signal)
        target=self.getLegalTarget1()
        if target:
            yield self.y_destroyCard(target)
        return True


"""
1A:[解放此卡]:让对方随机除外手牌1张
"""
class TributeRandomBanishEnemyHand(Effect):
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 2

    def y_cost(self,justCheck:bool,signal):
        enemyHandTotal=0
        for side in self.getEnemySideTuple():
            enemyHandTotal+=len(self.game.hands[side])
        if enemyHandTotal==0:
            return False
        if justCheck:
            return True
        successNum=yield self.y_tributeCard(self.owner)
        return successNum!=0

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True
        candidates=[]
        for side in self.getEnemySideTuple():
            candidates.extend(self.game.hands[side])
        if not candidates:
            return False
        import random as _r
        target=_r.choice(candidates)
        yield self.y_banishCard(target)
        return True


"""
1P:对方不能特殊召唤LV5以上的怪兽
"""
# 暂未实现:依赖 PLAYER_BUFF.cantSpecialSummonLv5Up + y_specialSummon 内拒绝 LV5+ 的检查
# class EnemyCantSpecialSummonLv5Up(Effect):
#     effType = EFF_TYPE.permanent
#     observeSignals = (LOCATION.monsterZone,[
#         Signal.AttachMonsterZone,
#         Signal.DetachMonsterZone,
#     ])
#     AI_HINT = [AI_HINT.permanent,AI_HINT.eraser]
#     EFF_POWER = 3
#
#     def y_signal(self,signal):
#         if isSignal(signal,Signal.DetachMonsterZone,self.owner):
#             yield self.y_removePlayerBuffEffectSource(self.getEnemySideTuple(),self.effUniID)
#             return
#
#         if not self.owner.isMonsterOnField():
#             return
#
#         yield self.y_addPlayerBuff(self.getEnemySideTuple(),PLAYER_BUFF.cantSpecialSummonLv5Up,
#                                    EFF_DURATION.fromSource,self.effUniID)


"""
1A:[支付LP 500]:让对方随机丢弃手牌1张
"""
class PayLP500RandomDiscardEnemy(Effect):
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 2

    def y_cost(self,justCheck:bool,signal):
        myLP=self.game.LPs[self.getSide()]
        if myLP<=500:
            return False
        enemyHandTotal=0
        for side in self.getEnemySideTuple():
            enemyHandTotal+=len(self.game.hands[side])
        if enemyHandTotal==0:
            return False
        if justCheck:
            return True
        self.game.damagePlayer(self.getSide(),500,False)
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True
        candidates=[]
        for side in self.getEnemySideTuple():
            candidates.extend(self.game.hands[side])
        if not candidates:
            return False
        import random as _r
        target=_r.choice(candidates)
        yield self.y_sendCardToGrave(target)
        return True


"""
1OT:<通常召唤时>:指定对方场上1只怪兽,本回合该怪兽不能攻击也不能发动效果
"""
# 暂未实现:依赖 CARD_BUFF.cantDeclareAttack(目前仅 PLAYER_BUFF 层有)+ 卡级宣言攻击拦截
# class NormalSummonLockEnemy(Effect):
#     effType = EFF_TYPE.optionalTrigger
#     observeSignals = (LOCATION.monsterZone,[Signal.NormalSummon])
#     AI_HINT = [AI_HINT.debuff]
#     EFF_POWER = 2
#
#     def y_cost(self,justCheck:bool,signal):
#         if not isSignal(signal,Signal.NormalSummon,self.owner):
#             return False
#         enemyMonsters=self.searchCards(LOCATION.monsterZone,self.getEnemySideTuple(),CARD_TYPE.monster,self)
#         if not enemyMonsters:
#             return False
#         if justCheck:
#             return True
#         target=yield self.y_select1Card(enemyMonsters,TITLE.target,self.getSide(),canCancel=True)
#         if not target:
#             return False
#         self.saveTarget1(target)
#         return True
#
#     def y_activate(self,justCheck:bool,signal):
#         if justCheck:
#             return True
#         target=self.getLegalTarget1()
#         if target:
#             yield self.y_silenceCard(target,EFF_DURATION.utilTurnEnds,self.effUniID)
#             yield self.y_addCardBuff(target,CARD_BUFF.cantDeclareAttack,
#                                      EFF_DURATION.utilTurnEnds,self.effUniID)
#         return True
