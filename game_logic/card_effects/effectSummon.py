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
1A:<手牌效果>:如果你没控制怪兽,无需祭品通常召唤此卡
"""
class NormalSummonNoTri(Effect):
    effType = EFF_TYPE.active

    activateLocation = LOCATION.hand

    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 2
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal):
        if self.game.monsters[self.getSide()]:
            return False

        if not self.checkCanNormalSummon(self.owner,tributeNumChange=-100):
            return False

        if justCheck:
            return True

        yield self.y_normalSummon(False,self.owner,tributeNumChange=-100)
        return True

"""
1A:<手牌效果>:当对方召唤怪兽时,特殊召唤此卡
"""
class OppoSummonSpecialSummon(Effect):
    effType = EFF_TYPE.trigger

    manaCost = 1

    observeSignals = (LOCATION.monsterZone,[Signal.Summon])

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 3
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        if isSignal(signal,Signal.Summon) and signal.card.side in self.getEnemySideTuple():
            pass
        else:
            return False

        if not self.freeMonsterSpace():
            return False

        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal):
        if self.owner.location!=LOCATION.hand:
            return False
        if justCheck:
            return True

        yield self.y_specialSummon(self.owner)
        return True


"""
1A:<手牌效果>:如果你控制的怪兽全是兽族,特殊召唤此卡
"""
class AllMonstersAreSpecialSummon(Effect):
    effType = EFF_TYPE.active
    activateLocation = LOCATION.hand

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 3
    def y_signal(self,signal):
        pass


    def y_activate(self,justCheck:bool,signal):
        myMonsters:List[Card]=self.searchCards(LOCATION.monsterZone,self.getSide(),CARD_TYPE.monster)
        if not myMonsters:
            return False

        for monster in myMonsters:
            if monster.race!=RACE.BEAST:
                return False

        if not self.freeMonsterSpace():
            return False

        if justCheck:
            return True

        yield self.y_specialSummon(self.owner)
        return True

"""
1T:<场上效果>[不限次数]:当我方怪兽特殊召唤时,生成并特殊召唤一只DragonBug
"""
class MeSpecialSummonWhile(Effect):
    effType = EFF_TYPE.trigger

    observeSignals = (LOCATION.monsterZone,[Signal.Summon])

    countLimit = COUNT_LIMIT.unlimited

    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 5
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        # 防止无限循环:DragonBug 被特殊召唤时不再触发此效果;owner 自己被特殊召唤也不再触发
        if not (isSignal(signal,Signal.SpecialSummon) and self.checkAlly(signal.card)):
            return False
        if signal.card.key == "DragonBug":
            return False
        if signal.card == self.owner:
            return False
        if not self.freeMonsterSpace():
            return False
        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True

        card=self.game.createCard("DragonBug",self.getSide())
        yield self.y_specialSummon(card)
        return True


"""
1A:<手牌效果>:对方手牌在4张以上时,将此卡无需祭品通常召唤
"""
class NormalSummonWithManyHands(Effect):
    effType = EFF_TYPE.active

    activateLocation = LOCATION.hand

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 2
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal):
        found=False
        for side in self.getEnemySideTuple():
            handcardNum=len(self.game.hands[side])
            if handcardNum>=4:
                found=True
                break

        if not found:
            return False

        if not self.checkCanNormalSummon(self.owner,tributeNumChange=-100):
            return False

        if justCheck:
            return True

        yield self.y_normalSummon(False,self.owner,tributeNumChange=-100)
        return True


"""
1A:<手牌效果>:对方手牌在4张以上时,将此卡特殊召唤
"""
class SpecailSummonSummonWithManyHands(Effect):
    effType = EFF_TYPE.active

    activateLocation = LOCATION.hand

    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 2
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal):
        found=False
        for side in self.getEnemySideTuple():
            handcardNum=len(self.game.hands[side])
            if handcardNum>=4:
                found=True
                break

        if not found:
            return False

        if not self.checkCanSpecialSummon(self.owner):
            return False

        if justCheck:
            return True

        yield self.y_specialSummon(self.owner)
        return True

"""
<手牌效果>对方场上有怪兽时,将此卡特殊召唤
"""
class SpecialSummonSummonWithMonsterOnField(Effect):
    effType = EFF_TYPE.active

    activateLocation = LOCATION.hand

    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 3
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal):
        found=False
        for side in self.getEnemySideTuple():
            monsterNum=len(self.game.monsters[side])
            if monsterNum>=1:
                found=True
                break

        if not found:
            return False

        if not self.checkCanSpecialSummon(self.owner):
            return False

        if justCheck:
            return True

        yield self.y_specialSummon(self.owner)
        return True




"""
[献祭场上的一只怪兽]:根据怪兽属性发动以下效果:
    ●风·水:获取对方场上攻击力最低的怪兽的控制权,直到回合结束
    ●炎·地:从卡组特殊召唤一只LV4以下的炎·地属性怪兽
"""
# class SplitEffect(Effect):
#     effType = EFF_TYPE.active
#
#     activateLocation = LOCATION.monsterZone
#
#     tributedATTR=0
#
#     AI_HINT = [AI_HINT.eraser]
#     EFF_POWER = 2
#     def y_signal(self,signal):
#         pass
#
#     def y_cost(self,justCheck:bool,signal):
#         def f(card):
#             return card.attr&(ATTR.WATER|ATTR.FIRE|ATTR.EARTH|ATTR.WIND)
#         myMonsters=self.searchCards(LOCATION.monsterZone,self.getSide(),CARD_TYPE.monster,self,f)
#         if not myMonsters:
#             return False
#         if justCheck:
#             return True
#
#         theTribute=yield self.y_select1Card(myMonsters,TITLE.tribute,self.getSide(),canCancel=True)
#         if not theTribute:
#             return False
#
#         successNum=yield self.y_tributeCard(theTribute)
#         if successNum!=0:
#             self.tributedATTR=theTribute.attr
#
#         return successNum!=0
#
#     def y_activate(self,justCheck:bool,signal):
#         if justCheck:
#             return True
#
#         if not self.tributedATTR:
#             return False
#
#         if self.tributedATTR & (ATTR.WIND|ATTR.WATER):
#             enemyMonsters=self.searchCards(LOCATION.monsterZone,self.getEnemySideTuple(),CARD_TYPE.monster,self)
#             enemy=yield self.y_select1Card(enemyMonsters,TITLE.changeController,self.getSide())
#             yield self.y_changeMonsterController(enemy)
#         if self.tributedATTR & (ATTR.FIRE|ATTR.EARTH):
#             #TODO
#             pass
#
#         return True



"""
<场上效果>[丢弃一张手牌]:从手卡·卡组特殊召唤一只LV8以下的不死族怪兽
"""
class DiscardSpecial(Effect):
    effType = EFF_TYPE.active

    activateLocation = LOCATION.monsterZone

    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 3
    def y_cost(self,justCheck:bool,signal):
        handcards=self.game.hands[self.getSide()]
        if not handcards:
            return False

        if justCheck:
            return True

        thecard=yield self.y_select1Card(handcards,TITLE.sendToGrave,self.getSide(),canCancel=True)
        if not thecard:
            return False
        successNum=yield self.y_sendCardToGrave(thecard)
        return successNum!=0

    def y_activate(self,justCheck:bool,signal):
        def f(c):
            return c.level<=8 and c.race==RACE.UNDEAD
        undeadMonsters=self.searchCards(LOCATION.hand+LOCATION.deck,self.getSide(),CARD_TYPE.monster,self,f)

        if not undeadMonsters:
            return False

        if justCheck:
            return True

        thecard=yield self.y_select1Card(undeadMonsters,TITLE.specialSummon,self.getSide())
        if thecard:
            yield self.y_specialSummon(thecard)
        return True

"""
<召唤成功时>:如果自己场上没有其他怪兽,从手卡特殊召唤一只LV4以下的怪兽
"""
class SummonAddSummon(Effect):
    effType = EFF_TYPE.trigger

    observeSignals = (LOCATION.monsterZone,[Signal.Summon])

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 3
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        if isSignal(signal,Signal.Summon,self.owner):
            pass
        else:return False

        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal):
        fieldMonsters=self.game.monsters[self.getSide()]
        if len(fieldMonsters)==1 and fieldMonsters[0]==self.owner:
            pass
        else:
            return False

        def f(card):
            return card.level<=4
        handMonsters=self.searchCards(LOCATION.hand,self.getSide(),CARD_TYPE.monster,self,f)
        if not handMonsters:
            return False

        if justCheck:
            return True

        thecard=yield self.y_select1Card(handMonsters,TITLE.specialSummon,self.getSide())
        if thecard:
            yield self.y_specialSummon(thecard)

        return True




"""
<墓地效果>:对方召唤怪兽时,此卡返回卡组,从墓地特殊召唤一只LV6以下的怪兽
"""
class ReturnSpecialSummon(Effect):
    effType = EFF_TYPE.trigger

    observeSignals = (LOCATION.grave,[Signal.Summon])

    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 2
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        if isSignal(signal,Signal.Summon) and signal.card.side!=self.getSide():
            pass
        else:
            return False

        def f(card):
            return card.level<=6

        graveMonsters=self.searchCards(LOCATION.grave,self.getSide(),CARD_TYPE.monster,self,f)

        if self.owner in graveMonsters:
            graveMonsters.remove(self.owner)

        if not graveMonsters:
            return False

        if justCheck:
            return True

        target=yield self.y_select1Card(graveMonsters,TITLE.specialSummon,self.getSide(),canCancel=True)
        if not target:
            return False

        self.saveTarget1(target)
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True

        yield self.y_returnCardToDeck(self.owner)

        target=self.getLegalTarget1()
        if target:
            yield self.y_specialSummon(target)

        return True




"""
1P:<手牌效果>:每次对方特殊召唤怪兽,此卡的等级下降1级
"""
class EnemySpecialDownLv(Effect):
    effType = EFF_TYPE.permanent

    observeSignals = (LOCATION.hand,[Signal.Summon])

    EFF_POWER = 1

    def y_signal(self,signal):
        if isSignal(signal,Signal.SpecialSummon) and signal.card.side in self.getEnemySideTuple():
            yield self.y_addCardData(self.owner,levelAdd=-1)


"""
<手牌效果>:当对方发动手牌·墓地的怪兽效果时,特殊召唤此卡
"""
class HandGraveActivateSpecial(Effect):
    effType = EFF_TYPE.trigger

    observeSignals = (LOCATION.hand,[Signal.BeforeActivateEffect])

    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 3

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            if isSignal(signal,Signal.BeforeActivateEffect) and signal.card.isMonster() and  signal.card.side!=self.getSide() and signal.card.location&(LOCATION.hand+LOCATION.grave)!=0:
                return True
            else:
                return False

        yield self.y_specialSummon(self.owner)
        return True



"""
<手牌效果>[除外墓地2只光属性怪兽]:从手牌特殊召唤此卡和另一张LV5光属性怪兽
"""
class SpecialSummonThisAnd(Effect):
    effType = EFF_TYPE.active

    activateLocation = LOCATION.hand
    manaCost = 2

    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 3
    def y_cost(self,justCheck:bool,signal:Signal.Signal):
        def f(card):
            return card.attr==ATTR.LIGHT
        graveMonsters=self.searchCards(LOCATION.grave,self.getSide(),CARD_TYPE.monster,self,f)
        if len(graveMonsters)<2:
            return

        if justCheck:
            return True

        twoMonsters=yield self.y_selectCards(graveMonsters,TITLE.banish,0,2,2,canCancel=True)
        if twoMonsters and len(twoMonsters)==2:
            banishNum=yield self.y_banishCard(twoMonsters)
            if banishNum==2:
                return True


    def y_activate(self,justCheck:bool,signal):
        def f(card):
            return card.attr==ATTR.LIGHT and card.level==5
        monsters=self.searchCards(LOCATION.hand,self.getSide(),CARD_TYPE.monster,self,f)
        if not monsters:
            return False
        if justCheck:
            return True

        monster=yield self.y_select1Card(monsters,TITLE.specialSummon,self.getSide())
        if not monster:
            return False

        summonList=[monster,self.owner]
        yield self.y_specialSummon(summonList)
        return True



"""
<手牌效果>[选场上一只守备表示怪兽]:该怪兽变为攻击表示,然后特殊召唤此卡
"""
class ChangeSpecialSummon(Effect):
    effType = EFF_TYPE.active
    activateLocation = LOCATION.hand

    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 3
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        def f(card):
            return card.form==FORM.defence
        targetMon=self.searchCards(LOCATION.monsterZone,-1,CARD_TYPE.monster,self,f)
        if not targetMon:
            return False

        if justCheck:
            return True

        target=yield self.y_select1Card(targetMon,TITLE.target,self.getSide(),canCancel=True)
        if not target:
            return False

        self.saveTarget1(target)
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True

        target=self.getLegalTarget1()
        if not target:
            return
        successNum=yield self.y_changeForm(target, FORM.attack)
        if successNum:
            yield self.y_specialSummon(self.owner)


"""
<被战斗破坏时>:从手牌或卡组特殊召唤一只LV4以下的不死族怪兽
"""
class DestroySummonFromHD(Effect):
    effType = EFF_TYPE.trigger

    observeSignals = (LOCATION.grave,[Signal.DestroyedByBattle])

    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 2

    def y_activate(self,justCheck:bool,signal):
        if isSignal(signal, Signal.DestroyedByBattle, self.owner):
            pass
        else:
            return False

        def cardFilter(card):
            return card.race==RACE.UNDEAD and card.level<=4

        cardList=self.searchCards(LOCATION.hand|LOCATION.deck,self.getSide(),CARD_TYPE.monster,self,cardFilter)
        if not cardList:
            return False
        if justCheck:
            return True

        thecard=yield self.y_select1Card(cardList,TITLE.specialSummon,self.getSide())
        yield self.y_specialSummon(thecard)
        return True


"""
<被破坏后>[决斗中只能使用一次]:结束阶段时特殊召唤此卡,{ATK}和{DEF}都变为100
"""
class DieSpecialSummon(Effect):
    effType = EFF_TYPE.trigger

    observeSignals = (LOCATION.grave,[Signal.Destroyed,Signal.TurnEnds])

    deathTurn=0
    countLimit = COUNT_LIMIT.onlyOncePerDuel

    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 2

    def y_signal(self,signal):
        if isSignal(signal,Signal.Destroyed,self.owner):
            self.deathTurn=self.game.curTurn

    def y_activate(self,justCheck:bool,signal):
        if isSignal(signal,Signal.TurnEnds) and self.deathTurn == self.game.curTurn:
            pass
        else:
            return False

        if self.owner.isOnField():
            WARNING_MSG("shouldnt on the field ",self.owner.getName())
            return False

        if justCheck:
            return True

        self.deathTurn=0
        yield self.y_specialSummon(self.owner)
        if self.owner.isMonsterOnField():
            yield self.y_changeCardData(self.owner,100,100)
        return True

    def y_locationChange(self,oldSide,oldLocation,newSide,newLocation):
        self.deathTurn=0


#发动后变成永续魔法卡,2回合后特殊召唤
# class BecomeMagicSummon(Effect):
#     effType = EFF_TYPE.active
#
#     activateLocation = LOCATION.hand
#     observeSignals = (LOCATION.spellTrapZone,[Signal.TurnEnds])
#
#     turnCnt=0
#
#     magicSummonisSetted=False
#
#     AI_HINT = [AI_HINT.eraser]
#     EFF_POWER = 1
#     def y_signal(self,signal):
#         if isSignal(signal,Signal.TurnEnds) and self.owner.isSpell() and self.magicSummonisSetted:
#             self.turnCnt+=1
#             if self.turnCnt>2:
#                 yield self.y_specialSummon(self.owner)
#
#     def y_cost(self,justCheck:bool,signal):
#         if justCheck:
#             return True
#         return True
#
#     def y_activate(self,justCheck:bool,signal):
#         if self.game.freeSpellSpace(self.getSide())==0:
#             return False
#         if justCheck:
#             return True
#         yield self.y_moveCardToSpellZone(self.owner)
#         self.magicSummonisSetted=True
#         self.turnCnt=0
#
#         return True
#
#     def y_locationChange(self,oldSide,oldLocation,newSide,newLocation):
#         if newLocation!=LOCATION.spellTrapZone:
#             self.magicSummonisSetted=False
#             self.turnCnt=0




#墓地中可发动,作为攻击力血量加1的装备卡装备到场上一只怪兽身上
# class GraveBecomeEquip(Effect):
#     effType = EFF_TYPE.active
#     activateLocation = LOCATION.grave
#
#     AI_HINT = [AI_HINT.enhance]
#     EFF_POWER = 1
#     def y_signal(self,signal):
#         pass
#
#     def y_cost(self,justCheck:bool,signal):
#         cardList=self.searchCards(LOCATION.monsterZone,-1,CARD_TYPE.monster,self)
#         if not cardList:
#             return False
#         if justCheck:
#             return True
#         target=yield self.y_select1Card(self.getSide(),TITLE.equip,cardList,canCancel=True)
#         if not target:
#             return False
#
#         self.saveTarget1(target)
#         return True
#
#     def y_activate(self,justCheck:bool,signal):
#
#         if justCheck:
#             return True
#
#         target=self.getLegalTarget1()
#         if not target:
#             return False
#
#         yield self.y_moveCardToSpellZone(self.owner,self.getSide(),target)
#         return True

#此卡装备的怪兽离开时可发动,特殊召唤此卡
# class EquipSpecialSummon(Effect):
#     effType = EFF_TYPE.optionalTrigger
#
#     manaCost = 2
#     observeSignals = (LOCATION.grave,[Signal.DetachMonsterZone])
#
#     AI_HINT = [AI_HINT.eraser]
#     EFF_POWER = 1
#     def y_signal(self,signal):
#         pass
#
#     def y_cost(self,justCheck:bool,signal):
#         if justCheck:
#             return True
#         return True
#
#     def y_activate(self,justCheck:bool,signal):
#         if justCheck:
#             return True
#         return True


"""
<手牌效果>:当手牌只有此卡时,可以只用一只祭品通常召唤此卡
"""
class OnlyHandNormalSummon(Effect):
    effType = EFF_TYPE.active
    activateLocation = LOCATION.hand

    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 1  # 条件苛刻(手上必须只有此卡),收益仅为省祭品
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        if len(self.game.hands[self.getSide()])==1 and self.game.hands[self.getSide()][0]==self.owner:
            pass
        else:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal):
        result=yield self.y_normalSummon(justCheck,self.owner,self.getSide(),True,1)
        return result


#此回合增加一次通常召唤次数
# class NormalSummonAdd(Effect):
#     effType = EFF_TYPE.active
#
#     manaCost = 1
#     AI_HINT = [AI_HINT.summoner]
#     EFF_POWER = 1
#     def y_signal(self,signal):
#         pass
#
#     def y_cost(self,justCheck:bool,signal):
#         if justCheck:
#             return True
#         return True
#
#     def y_activate(self,justCheck:bool,signal):
#         self.y_addPlayerBuff()
#         if justCheck:
#             return True
#         return True

#<通常召唤成功时>:从卡组·手牌特殊召唤不超过对方场上怪兽数量的LV4以下的怪兽
class NormalSummonMaxSpecial(Effect):
    effType = EFF_TYPE.optionalTrigger

    observeSignals = (LOCATION.monsterZone,[Signal.NormalSummon])

    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 4

    def y_activate(self,justCheck:bool,signal):
        if isSignal(signal,Signal.NormalSummon,self.owner):
            pass
        else:
            return False
        enemyMonsters=self.searchCards(LOCATION.monsterZone,self.getEnemySideTuple(),CARD_TYPE.monster)
        enemyCardsNum=len(enemyMonsters)
        if enemyCardsNum<=0:
            return False

        def f(card:Card):
            return card.checkBuffCanSpecialSummon() and card.level<=4

        canSummonCards=self.searchCards(LOCATION.deck+LOCATION.hand,self.getSide(),CARD_TYPE.monster,self,f)

        if not canSummonCards:
            return False

        if justCheck:
            return True

        summonCards=yield self.y_selectCards(canSummonCards,TITLE.specialSummon,self.getSide(),0,enemyCardsNum)
        if summonCards:
            yield self.y_specialSummon(summonCards)
        return True




#<场上效果>:对方把怪兽召唤成功时,选择我方卡组中一只怪兽除外或者送入墓地
class EnemySummonSendOrBanish(Effect):
    effType = EFF_TYPE.trigger

    observeSignals = (LOCATION.monsterZone,[Signal.Summon])

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 2
    def y_activate(self,justCheck:bool,signal):
        if isSignal(signal,Signal.Summon) and signal.card.side!=self.getSide():
            pass
        else:
            return False

        cards=self.searchCards(LOCATION.deck,self.getSide(),CARD_TYPE.monster,self,lambda card:card.series)

        if not cards:
            return False

        if justCheck:
            return True

        option,card=yield self.duel.y_showCardSelectorPanel(cards,TITLE.target,self.getSide(),[I2.sendToGrave,I2.banish,I2.CANCEL])
        if card:
            if option==0:
                yield self.y_sendCardToGrave(card)
            if option==1:
                yield self.y_banishCard(card)

        return True



#<场上效果>:从卡组内选择两只LV4以下的兽族怪兽,分别特殊召唤到我方和对方场上
class Summon2Beast(Effect):
    effType = EFF_TYPE.active

    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 2

    selectedOpposide=0

    def y_cost(self,justCheck:bool,signal:Signal.Signal):
        def oppoFilter(side):
            return self.game.freeMonsterSpace(side)!=0
        opposides=self.filterEnemySide(oppoFilter)
        if not opposides:
            return False

        if justCheck:
            return True

        self.selectedOpposide=yield self.y_select1EnemySide(opposides)
        if not self.selectedOpposide:
            return False
        return True

    def y_activate(self,justCheck:bool,signal):
        if self.freeMonsterSpace()<1:
            return False

        def f(card:Card):
            return card.race==RACE.BEAST and card.level<=4 and card.checkBuffCanSpecialSummon()
        beastCards=self.searchCards(LOCATION.deck,self.getSide(),CARD_TYPE.monster,self,f)

        if len(beastCards)<2:
            return False

        if justCheck:
            return True

        myBeast=yield self.y_select1Card(beastCards,TITLE.specialSummon,self.getSide(),canCancel=False)
        if myBeast:
            beastCards.remove(myBeast)
        enemyBeast=yield self.y_select1Card(beastCards,TITLE.specialSummonToEnemy,self.getSide(),canCancel=False)


        if myBeast:
            yield self.y_specialSummon(myBeast)
        if enemyBeast:
            yield self.y_specialSummon(enemyBeast,self.selectedOpposide)
        return True



"""
<手牌效果>:当我方受到战斗伤害时,特殊召唤此卡
"""
class SpecialSummonWhileBattleDamage(Effect):
    effType = EFF_TYPE.optionalTrigger

    observeSignals = (LOCATION.hand,[Signal.PlayerLPLoseByBattle])

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 3
    def y_signal(self,signal):
        pass

    def y_cost(self, justCheck:bool, signal):
        if not isSignal(signal, Signal.PlayerLPLoseByBattle):
            return False
        if signal.receiverPlayer!=self.getSide():
            return False

        if not self.freeMonsterSpace():
            return False

        if justCheck:
            return True

        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True

        if self.owner.location==LOCATION.hand:
            yield self.y_specialSummon(self.owner)
        return True


"""
<手牌·墓地效果>:当你的兽族怪兽被破坏时,此卡特殊召唤
"""
class monsterDestroySummon(Effect):
    effType = EFF_TYPE.optionalTrigger

    observeSignals = (LOCATION.hand+LOCATION.grave,[Signal.Destroyed])

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 3
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal:Signal.Destroyed):
        if isSignal(signal,Signal.Destroyed) and signal.card.side==self.getSide() and signal.card.race==RACE.BEAST and signal.card!=self.owner:
            pass
        else:
            return False

        if not self.freeMonsterSpace():
            return False

        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True

        yield self.y_specialSummon(self.owner)
        return True




"""
<场上效果>:如果你的墓地内只有一张怪兽卡没有其他卡,额外召唤该怪兽
"""
class GraveOnly1MonsterESummon(Effect):
    effType = EFF_TYPE.active

    activateLocation = LOCATION.monsterZone

    AI_HINT = [AI_HINT.eraser,AI_HINT.botDontUse]
    EFF_POWER = 1

    def y_activate(self,justCheck:bool,signal):
        graveCards=self.game.graves[self.getSide()]

        if len(graveCards)==1 and graveCards[0].isMonster() and graveCards[0].canSpecialSummon():
            pass
        else:
            return False

        if justCheck:
            return True

        yield self.y_extraSummon(False,graveCards[0])
        return True




"""
<战斗效果>:此卡战斗破坏怪兽时,从卡组特殊召唤一只LV4以下的炎属性怪兽
"""
class attackDestroySummon(Effect):
    effType = EFF_TYPE.trigger

    observeSignals = (LOCATION.monsterZone,[Signal.DestroyedByBattle])

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 3
    def y_signal(self,signal):
        pass


    def y_activate(self,justCheck:bool,signal:Signal.DestroyedByBattle):
        if isSignal(signal,Signal.DestroyedByBattle) and signal.reasonCard==self.owner:
            pass
        else:
            return False

        def f(card):
            return card.attr==ATTR.FIRE and card.level<=4

        monsters=self.searchCards(LOCATION.deck,self.getSide(),CARD_TYPE.monster,self,f)

        if not monsters:
            return False

        if justCheck:
            return True

        target=yield self.y_select1Card(monsters,TITLE.specialSummon,canCancel=False)

        if target:
            yield self.y_specialSummon(target)
        return True




"""
<手牌效果>:额外召唤此卡
"""
class extraSummonFromHand(Effect):
    effType = EFF_TYPE.active


    activateLocation = LOCATION.hand
    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 3

    def y_activate(self,justCheck:bool,signal):
        if not self.checkCanExtraSummon(self.owner):
            return
        if justCheck:
            return True
        yield self.y_extraSummon(False,self.owner)
        return True





"""
<墓地效果>[从手牌丢弃一只LV7以上的怪兽]:特殊召唤此卡
"""
class paohulong_effect1(Effect):
    effType = EFF_TYPE.active

    activateLocation = LOCATION.grave

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 2
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        def f(card):
            return card.isMonster() and card.level>=7

        handMonsters=self.searchCards(LOCATION.hand,self.getSide(),CARD_TYPE.monster,None,f)
        if not handMonsters:
            return False

        if justCheck:
            return True

        card=yield self.y_select1Card(handMonsters,TITLE.sendToGrave,canCancel=True)
        if not card:
            return False

        isSuccess=yield self.y_sendCardToGrave(card)
        return isSuccess

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True

        yield self.y_specialSummon(self.owner)
        return True


"""
<通常召唤后>:特殊召唤手牌·墓地的一只LV4以下的怪兽
"""
class normalSummonSpecial(Effect):
    effType = EFF_TYPE.optionalTrigger

    observeSignals = (LOCATION.monsterZone,[Signal.NormalSummon])

    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 3
    def y_cost(self,justCheck:bool,signal):
        if isSignal(signal,Signal.NormalSummon,self.owner):
            pass
        else:
            return False

        def f(card):
            return card.level<=4

        num=9999
        if justCheck:
            num=1
        availMonsters=self.searchCards(LOCATION.hand+LOCATION.grave,self.getSide(),CARD_TYPE.monster,self,f,maxFoundNum=num)
        if not availMonsters:
            return False

        if justCheck:
            return True

        target=yield self.y_select1Card(availMonsters,TITLE.specialSummon,canCancel=True)
        if target:
            self.saveTarget1(target)
            return True
        return False

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True

        target=self.getLegalTarget1()
        if target:
            yield self.y_specialSummon(target)
        return True

"""
<手牌·墓地效果>[献祭一只龙族怪兽]:额外召唤此卡
"""
class tributeExtraSummonFromHG(Effect):
    effType = EFF_TYPE.active

    activateLocation = LOCATION.hand+LOCATION.grave

    AI_HINT = [AI_HINT.summonSelf]
    EFF_POWER = 2

    def y_cost(self,justCheck:bool,signal):
        def f(card):
            return card.race==RACE.DRAGON
        monsters=self.searchCards(LOCATION.monsterZone,self.getSide(),CARD_TYPE.monster,None,f)

        if not monsters:
            return False


        if justCheck:
            return True

        tributeTarget=yield self.y_select1Card(monsters,TITLE.tribute,canCancel=True)
        if tributeTarget:
            successNum=yield self.y_tributeCard(tributeTarget)
            if successNum:
                return True
        return False

    def y_activate(self,justCheck:bool,signal):
        if not self.checkCanExtraSummon(self.owner):
            return
        if justCheck:
            return True

        yield self.y_extraSummon(False,self.owner)
        return True

"""
<手牌·墓地效果>:当你控制龙族怪兽时,此卡特殊召唤
"""
class voidSummonFromHG(Effect):
    effType = EFF_TYPE.active

    activateLocation = LOCATION.hand+LOCATION.grave

    AI_HINT = [AI_HINT.summonSelf]
    EFF_POWER = 3

    def y_cost(self,justCheck:bool,signal):
        dragons=self.searchCards(LOCATION.monsterZone,self.getSide(),CARD_TYPE.monster,None,lambda card:card.race==RACE.DRAGON)

        if not dragons:
            return False

        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True

        yield self.y_specialSummon(self.owner)
        return True


"""
<手牌效果>:如果对方墓地没有怪兽卡存在,此卡特殊召唤
"""



"""
<场上效果>:回合结束时,特殊召唤墓地一只LV4以下的XX族怪兽
"""




"""
<手牌效果>:对方控制2只以上怪兽时,无需祭品通常召唤此卡
"""
class Enemy2MonstersSummon(Effect):
    effType = EFF_TYPE.active

    activateLocation = LOCATION.hand

    AI_HINT = [AI_HINT.summonSelf]
    EFF_POWER = 2
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        enemyMonsters=self.searchCards(LOCATION.monsterZone,self.getEnemySideTuple(),CARD_TYPE.monster)
        if len(enemyMonsters)<2:
            return


        if not self.checkCanNormalSummon(self.owner):
            return

        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal):
        isSuccess=yield self.y_normalSummon(justCheck,self.owner,costNormalSummonChance=True,tributeNumChange=-1000)
        return isSuccess

# ============================================================
# 以下为新增召唤类效果 x10
# ============================================================


"""
A:<手牌效果>:我方LP不足最大LP的一半时,从手牌将此卡特殊召唤
"""
class LPBelowHalfSummon(Effect):
    effType = EFF_TYPE.active

    activateLocation = LOCATION.hand

    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 2

    def y_activate(self, justCheck: bool, signal):
        maxLP = self.duel.INIT_LP
        curLP = self.game.LPs[self.getSide()]
        if curLP >= maxLP // 2:
            return False

        if self.game.freeMonsterSpace(self.getSide()) == 0:
            return False

        if justCheck:
            return True

        yield self.y_specialSummon(self.owner)
        return True


"""
A:<手牌效果>[除外手牌中一只与此卡同族的怪兽]:从手牌将此卡特殊召唤
"""
class BanishSelfSummon(Effect):
    effType = EFF_TYPE.active

    activateLocation = LOCATION.hand

    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 2

    def y_cost(self, justCheck: bool, signal):
        def f(c):
            return c.race == self.owner.race and c != self.owner

        sameRaceHand = self.searchCards(LOCATION.hand, self.getSide(), CARD_TYPE.monster, self, f)
        if not sameRaceHand:
            return False

        if self.game.freeMonsterSpace(self.getSide()) == 0:
            return False

        if justCheck:
            return True

        target = yield self.y_select1Card(sameRaceHand, TITLE.banish, canCancel=True)
        if not target:
            return False

        yield self.y_banishCard(target)
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck:
            return True

        yield self.y_specialSummon(self.owner)
        return True


"""
<手牌效果>:对方怪兽攻击时,将此卡从手牌特殊召唤
"""
class EnemyAttackSummonFromHand(Effect):
    effType = EFF_TYPE.optionalTrigger

    observeSignals = (LOCATION.hand, [Signal.RequestBattle])

    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 3

    def y_cost(self, justCheck: bool, signal: Signal.RequestBattle):
        if isSignal(signal, Signal.RequestBattle) and signal.attackerCard.side in self.getEnemySideTuple():
            pass
        else:
            return False

        if self.game.freeMonsterSpace(self.getSide()) == 0:
            return False

        if justCheck:
            return True
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck:
            return True

        yield self.y_specialSummon(self.owner)
        return True



"""
<场上效果>:当此卡被效果破坏时,从卡组特殊召唤一只4级以下与此卡同属性的怪兽
"""
class EffectDestroyedSummonFromDeck(Effect):
    effType = EFF_TYPE.trigger

    observeSignals = (LOCATION.monsterZone, [Signal.DestroyedOnFieldByEffect])

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 3

    def y_cost(self, justCheck: bool, signal: Signal.DestroyedOnFieldByEffect):
        if isSignal(signal, Signal.DestroyedOnFieldByEffect, self.owner):
            pass
        else:
            return False

        if justCheck:
            return True
        return True

    def y_activate(self, justCheck: bool, signal):
        attr = self.owner.attr

        def f(c):
            return c.level <= 4 and c.attr == attr

        deckMonsters = self.searchCards(LOCATION.deck, self.getSide(), CARD_TYPE.monster, self, f)
        if not deckMonsters:
            return False

        if justCheck:
            return True

        target = yield self.y_select1Card(deckMonsters, TITLE.specialSummon)
        if target:
            yield self.y_specialSummon(target)
        return True


"""
<手牌效果>:[如果此回合我方已经召唤了2次以上]:从手牌将此卡特殊召唤
<Hand Effect>:[If you have Summoned 2 or more times this turn]:Special Summon this card from your hand.
"""
# class SummonCounterSummon(Effect):
#     effType = EFF_TYPE.active
#
#     activateLocation = LOCATION.hand
#
#     AI_HINT = [AI_HINT.summoner]
#     EFF_POWER = 1
#
#     def y_activate(self, justCheck: bool, signal):
#         if self.game.summonCountThisTurn[self.getSide()] < 2:
#             return False
#
#         if self.game.freeMonsterSpace(self.getSide()) == 0:
#             return False
#
#         if justCheck:
#             return True
#
#         yield self.y_specialSummon(self.owner)
#         return True


"""
<墓地效果>[决斗中只能发动1次]:当我方发动魔法卡时,从墓地将此卡特殊召唤
"""
class SpellActivateSummon(Effect):
    effType = EFF_TYPE.optionalTrigger

    countLimit = COUNT_LIMIT.onlyOncePerDuel
    observeSignals = (LOCATION.grave, [Signal.ActivateSpellFinish])

    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 2

    def y_cost(self, justCheck: bool, signal):
        if isSignal(signal, Signal.ActivateSpellFinish) and signal.card.side == self.getSide():
            pass
        else:
            return False

        if self.game.freeMonsterSpace(self.getSide()) == 0:
            return False

        if justCheck:
            return True
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck:
            return True

        yield self.y_specialSummon(self.owner)
        return True


"""
<手牌效果>[献祭我方场上一只3级以下的怪兽]:如果我方怪兽区已满,从手牌将此卡特殊召唤
"""
class FullFieldSummonSwap(Effect):
    effType = EFF_TYPE.active

    activateLocation = LOCATION.hand

    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 2

    def y_cost(self, justCheck: bool, signal):
        if self.game.freeMonsterSpace(self.getSide()) != 0:
            return False

        def f(c):
            return c.level <= 3

        lowMonsters = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self, f)
        if not lowMonsters:
            return False

        if justCheck:
            return True

        target = yield self.y_select1Card(lowMonsters, TITLE.tribute, canCancel=True)
        if not target:
            return False

        successNum = yield self.y_tributeCard(target)
        return successNum != 0

    def y_activate(self, justCheck: bool, signal):
        if justCheck:
            return True

        yield self.y_specialSummon(self.owner)
        return True


"""
<场上效果>:当我方回合结束时,从墓地特殊召唤一只5级以下的暗属性怪兽
"""
class TurnEndSummonFromGrave(Effect):
    effType = EFF_TYPE.trigger

    countLimit = COUNT_LIMIT.oncePerTurn
    observeSignals = (LOCATION.monsterZone, [Signal.TurnEnds])

    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 3

    def y_cost(self, justCheck: bool, signal):
        if not isSignal(signal, Signal.TurnEnds):
            return False

        if self.game.whoseTurn != self.getSide():
            return False

        def f(c):
            return c.level <= 5 and c.attr == ATTR.DARK

        graveMonsters = self.searchCards(LOCATION.grave, self.getSide(), CARD_TYPE.monster, self, f)
        if not graveMonsters:
            return False

        if self.game.freeMonsterSpace(self.getSide()) == 0:
            return False

        if justCheck:
            return True

        target = yield self.y_select1Card(graveMonsters, TITLE.specialSummon, canCancel=True)
        if not target:
            return False

        self.saveTarget1(target)
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck:
            return True

        target = self.getLegalTarget1()
        if target:
            yield self.y_specialSummon(target)
        return True


"""
<墓地效果>[除外墓地中2只其他怪兽]:特殊召唤此卡
"""
class BanishRevive(Effect):
    effType = EFF_TYPE.active

    activateLocation = LOCATION.grave

    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 2

    def y_cost(self, justCheck: bool, signal):
        def f(c):
            return c != self.owner

        graveMonsters = self.sear

# ============================================================
# 新增效果实现
# ============================================================

"""
1OT:<通常召唤时>:从卡组顶5张中发现一只与此卡同种族的怪兽加入手牌
"""
class NormalSummonPeek5SameRace(Effect):
    effType = EFF_TYPE.optionalTrigger
    observeSignals = (LOCATION.monsterZone,[Signal.NormalSummon])
    AI_HINT = [AI_HINT.searchMonster] if hasattr(AI_HINT,"searchMonster") else [AI_HINT.summoner]
    EFF_POWER = 2

    def y_cost(self,justCheck:bool,signal):
        if not isSignal(signal,Signal.NormalSummon,self.owner):
            return False
        deckCards=self.game.decks[self.getSide()]
        if not deckCards:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True
        deckCards=self.game.decks[self.getSide()]
        if not deckCards:
            return False
        pickNum=min(5,len(deckCards))
        top=[deckCards[len(deckCards)-1-i] for i in range(pickNum)]
        myRace=self.owner.race
        sameRace=[c for c in top if c.cardType&CARD_TYPE.monster and c.race==myRace]
        if sameRace:
            theCard=yield self.y_select1Card(sameRace,TITLE.addToHand,self.getSide(),canCancel=True)
            if theCard:
                yield self.y_returnCardToHand(theCard,self.getSide())
        import random as _r
        _r.shuffle(deckCards)
        return True


"""
1T:<被通常召唤时>:若对方场上怪兽数多于我方,从手牌特殊召唤一只LV4以下的怪兽
"""
class NormalSummonedBehindSummonLv4(Effect):
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone,[Signal.NormalSummon])
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 2

    def y_cost(self,justCheck:bool,signal):
        if not isSignal(signal,Signal.NormalSummon,self.owner):
            return False
        myCount=len(self.searchCards(LOCATION.monsterZone,self.getSide(),CARD_TYPE.monster,None))
        enCount=len(self.searchCards(LOCATION.monsterZone,self.getEnemySideTuple(),CARD_TYPE.monster,None))
        if enCount<=myCount:
            return False
        if self.game.freeMonsterSpace(self.getSide())==0:
            return False
        handLv4=self.searchCards(LOCATION.hand,self.getSide(),CARD_TYPE.monster,self,
                                 lambda c:c.level<=4 and c.canSpecialSummon())
        if not handLv4:
            return False
        if justCheck:
            return True
        target=yield self.y_select1Card(handLv4,TITLE.specialSummon,self.getSide(),canCancel=True)
        if not target:
            return False
        self.saveTarget1(target)
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True
        target=self.getLegalTarget1()
        if target:
            yield self.y_specialSummon(target)
        return True


"""
1OT:<此卡被解放时>:从墓地特殊召唤一只LV3以下的怪兽
"""
class TributedReviveLv3(Effect):
    effType = EFF_TYPE.optionalTrigger
    observeSignals = (LOCATION.grave,[Signal.Tributed])
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 2

    def y_cost(self,justCheck:bool,signal):
        if not isSignal(signal,Signal.Tributed,self.owner):
            return False
        if self.game.freeMonsterSpace(self.getSide())==0:
            return False
        graveLv3=self.searchCards(LOCATION.grave,self.getSide(),CARD_TYPE.monster,self,
                                  lambda c:c.level<=3 and c is not self.owner and c.canSpecialSummon())
        if not graveLv3:
            return False
        if justCheck:
            return True
        target=yield self.y_select1Card(graveLv3,TITLE.specialSummon,self.getSide(),canCancel=True)
        if not target:
            return False
        self.saveTarget1(target)
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True
        target=self.getLegalTarget1()
        if target:
            yield self.y_specialSummon(target)
        return True


"""
1A:<场上效果>[解放此卡]:从手牌特殊召唤一只LV5以上的怪兽
"""
class TributeSummonHandLv5Up(Effect):
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 3

    def y_cost(self,justCheck:bool,signal):
        handLv5=self.searchCards(LOCATION.hand,self.getSide(),CARD_TYPE.monster,self,
                                 lambda c:c.level>=5 and c.canSpecialSummon())
        if not handLv5:
            return False
        if justCheck:
            return True
        target=yield self.y_select1Card(handLv5,TITLE.specialSummon,self.getSide(),canCancel=True)
        if not target:
            return False
        successNum=yield self.y_tributeCard(self.owner)
        if successNum==0:
            return False
        self.saveTarget1(target)
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True
        target=self.getLegalTarget1()
        if target:
            yield self.y_specialSummon(target)
        return True


"""
1T:<被特殊召唤时>:抽一张卡
"""
class SpecialSummonedDraw1(Effect):
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone,[Signal.SpecialSummon])
    AI_HINT = [AI_HINT.drawCard]
    EFF_POWER = 2

    def y_cost(self,justCheck:bool,signal):
        if not isSignal(signal,Signal.SpecialSummon,self.owner):
            return False
        if not self.game.decks[self.getSide()]:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True
        yield self.y_drawCard(self.getSide())
        return True


"""
1OT:<手牌效果>:对方通常召唤怪兽时,特殊召唤此卡
"""
class OppNormalSummonSelfSummon(Effect):
    effType = EFF_TYPE.optionalTrigger
    observeSignals = (LOCATION.hand,[Signal.NormalSummon])
    AI_HINT = [AI_HINT.summonSelf]
    EFF_POWER = 2

    def y_cost(self,justCheck:bool,signal):
        if not isSignal(signal,Signal.NormalSummon):
            return False
        if signal.card is None or signal.card.side==self.getSide():
            return False
        if self.game.freeMonsterSpace(self.getSide())==0:
            return False
        if not self.owner.canSpecialSummon():
            return False
        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True
        yield self.y_specialSummon(self.owner)
        return True


"""
1A:<手牌效果>[解放我方场上1只怪兽]:特殊召唤此卡
"""
class TributeMyMonsterSelfSummon(Effect):
    effType = EFF_TYPE.active
    activateLocation = LOCATION.hand
    AI_HINT = [AI_HINT.summonSelf]
    EFF_POWER = 2

    def y_cost(self,justCheck:bool,signal):
        myMonsters=self.searchCards(LOCATION.monsterZone,self.getSide(),CARD_TYPE.monster,self)
        if not myMonsters:
            return False
        if not self.owner.canSpecialSummon():
            return False
        if justCheck:
            return True
        target=yield self.y_select1Card(myMonsters,TITLE.tribute,self.getSide(),canCancel=True)
        if not target:
            return False
        successNum=yield self.y_tributeCard(target)
        return successNum!=0

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True
        if self.game.freeMonsterSpace(self.getSide())==0:
            return False
        yield self.y_specialSummon(self.owner)
        return True


"""
1A:<墓地效果>[除外墓地中3只其他怪兽]:从手牌或墓地特殊召唤此卡
"""
class GraveBanish3SelfRevive(Effect):
    effType = EFF_TYPE.active
    activateLocation = LOCATION.grave
    AI_HINT = [AI_HINT.summonSelf]
    EFF_POWER = 3

    def y_cost(self,justCheck:bool,signal):
        graveOthers=self.searchCards(LOCATION.grave,self.getSide(),CARD_TYPE.monster,self,
                                     lambda c:c is not self.owner)
        if len(graveOthers)<3:
            return False
        if self.game.freeMonsterSpace(self.getSide())==0:
            return False
        if not self.owner.canSpecialSummon():
            return False
        if justCheck:
            return True
        chosen=[]
        pool=list(graveOthers)
        for _ in range(3):
            if not pool:
                return False
            target=yield self.y_select1Card(pool,TITLE.banish,self.getSide(),canCancel=True)
            if not target:
                return False
            chosen.append(target)
            pool.remove(target)
        for c in chosen:
            yield self.y_banishCard(c)
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True
        yield self.y_specialSummon(self.owner)
        return True


"""
1OT:<手牌效果>[不限次数]:我方怪兽被破坏时,特殊召唤此卡
"""
class FriendDestroyedSelfSummon(Effect):
    effType = EFF_TYPE.optionalTrigger
    observeSignals = (LOCATION.hand,[Signal.Destroyed])
    countLimit = COUNT_LIMIT.unlimited
    AI_HINT = [AI_HINT.summonSelf]
    EFF_POWER = 2

    def y_cost(self,justCheck:bool,signal):
        if not isSignal(signal,Signal.Destroyed):
            return False
        if signal.card is None or signal.card is self.owner:
            return False
        if signal.card.side!=self.getSide():
            return False
        if self.game.freeMonsterSpace(self.getSide())==0:
            return False
        if not self.owner.canSpecialSummon():
            return False
        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True
        yield self.y_specialSummon(self.owner)
        return True


"""
1T:<场上效果>:我方回合开始时,从卡组顶检查3张,特殊召唤其中1只LV4以下的怪兽,其余送去墓地
"""
class MyTurnStartTopPeek3SummonRest(Effect):
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone,[Signal.DrawPhase])
    countLimit = COUNT_LIMIT.oncePerTurn
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 3

    def y_cost(self,justCheck:bool,signal):
        if not isSignal(signal,Signal.DrawPhase):
            return False
        if self.game.whoseTurn!=self.getSide():
            return False
        deckCards=self.game.decks[self.getSide()]
        if not deckCards:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True
        deckCards=self.game.decks[self.getSide()]
        if not deckCards:
            return False
        pickNum=min(3,len(deckCards))
        top=[deckCards[len(deckCards)-1-i] for i in range(pickNum)]
        lv4Monsters=[c for c in top if c.cardType&CARD_TYPE.monster and c.level<=4 and c.canSpecialSummon()]
        summoned=None
        if lv4Monsters and self.game.freeMonsterSpace(self.getSide())>0:
            summoned=yield self.y_select1Card(lv4Monsters,TITLE.specialSummon,self.getSide(),canCancel=True)
            if summoned:
                yield self.y_specialSummon(summoned)
        rest=[c for c in top if c is not summoned]
        if rest:
            yield self.y_sendCardToGrave(rest)
        return True
