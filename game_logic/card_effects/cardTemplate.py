# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *


"""
卡牌设计注意事项:

不要加入取对象和不取对象的设计
    要分清"取对象"和"不取对象"是十分伤脑筋的事情
    应该用效果免疫和强力效果(无视效果免疫)来取代

尽量减少"康"的设计,比如"神之宣告"
    "康"会对娱乐卡组造成毁灭性的破坏,要让娱乐卡组也有一战之力

检索和特殊召唤相关的牌要加入费用
    为了不让游戏在第一回合就结束

尽量不要有"减少费用"的效果,特别是给很容易出的牌
    因为出费用的初衷就是为了降速,减费效果和降速相悖

效果对象不要有"系列"和"卡名"的限制,应该用种族和属性来限制
    因为未来会出随机组卡的轮抽赛制
    
如果是可爱风格系列的卡片,要降低卡牌使用难度,不要加入深度思考的设计,而是采用大量的随机元素,不要加入精准检索,而是让玩法变成"哪里亮了点哪里"

    
"""

"""
this file is activated by "mergeCardsModule("cards.cardPack1")"
"""


class EffectTemple(Effect):
    effType = EFF_TYPE.active + EFF_TYPE.optionalTrigger

    manaCost = 0
    """
    use count per turn
    """
    countLimit = COUNT_LIMIT.oncePerTurn
    """
    Display other names on the operation panel.
    """
    specificOperate = OPERATE.activateEffect_specialSummon
    """
    active effect can be activated in this location,remain 0 for auto generation
    """
    activateLocation = LOCATION.monsterZone
    """
    This effect only accepts signals when it is in the location of observeSignals[0].
    
    Accepts signals are in observeSignals[1] and their father signals.
    """
    observeSignals = (LOCATION.monsterZone|LOCATION.grave, [Signal.TurnEnds])

    """
    hints for bot ai
    """
    AI_HINT:List[AI_HINT] = []
    EFF_POWER = 0

    """
    The label of the effect, with no practical use.
    """
    TAGS = [EFF_TAG.specialSummon,EFF_TAG.destroyMonster]

    """
    on receiving a signal,called before y_cost
    """
    def y_signal(self, signal:Signal.Signal):
        pass

    """
    "justCheck" means that it's just a test to see if it can be executed, with no real effect.
    
    This effect can only be activated when both "y_cost(True,signal)" and "y_activate(True,signal)" return True
    
    When this effect is activated,"y_cost(False,signal)" and "y_activate(False,signal)" will be called
    
    There should be no yield methods before "if justCheck:return True"
    """

    def y_cost(self, justCheck: bool,signal:Signal.Signal):
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck: bool,signal:Signal.Signal):
        if justCheck:
            return True
        return True

    """
    Always called when moving to new location
    Called earlier than y_signal
    """
    def y_locationChange(self,oldSide:int,oldLocation:LOCATION,newSide:int,newLocation:LOCATION):
        pass








class Wyvern_effect1(Effect):
    effType = EFF_TYPE.instant

    observeSignals = (LOCATION.monsterZone,[Signal.InBattle])

    AI_HINT = [AI_HINT.eraser]
    AI_POWER = 1
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        if isSignal(signal,Signal.InBattle) and signal.attackerCard==self.owner:
            pass
        else:
            return False

        # def f(card):
        #     return card.race==RACE.DRAGON
        graveMonsters=self.searchCards(LOCATION.grave,self.getSide(),CARD_TYPE.monster,self)
        if not graveMonsters:
            return False

        if justCheck:
            return True

        thedragon=yield self.y_select1Card(graveMonsters,TITLE.specialSummon,canCancel=False)
        self.saveTarget1(thedragon)
        return True

    def y_activate(self,justCheck:bool,signal):

        if justCheck:
            return True

        enemySide=yield self.y_select1EnemySide()
        thedragon=self.getLegalTarget1()
        if thedragon:
            yield self.y_specialSummon(thedragon,enemySide)

        return True

class GiantBeetle1(Card):
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(GiantBeetle_effect1)

class GiantBeetle_effect1(Effect):
    effType = EFF_TYPE.active

    activateLocation = LOCATION.monsterZone

    AI_HINT = [AI_HINT.eraser]
    AI_POWER = 1
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True
        DEBUG_MSG("effect giant")
        return True

class Phoenix1(Card):
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(dropHandCardDestroy)







"""
<墓地效果>[Cost:除外此卡]:当对方发动魔法或怪兽效果时,选一只你的怪兽的{ATK}{DEF}恢复到原本数值
"""


class GiveMeA(Effect):
    effType = EFF_TYPE.active

    activateLocation = LOCATION.monsterZone

    AI_HINT = [AI_HINT.enhance]
    AI_POWER = 1
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal:Signal.BattlePreData):
        if justCheck:
            return True

        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True

        return True


class EffSelector(Effect):
    effType = EFF_TYPE.active


    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 1
    def y_signal(self,signal):
        pass

    selectedOption=0
    def y_cost(self,justCheck:bool,signal):
        if justCheck:
            return True
        option=yield self.y_showOptionsPopUp(TITLE.selectEffect,self.getDescribe(),self.getSide(),["A","B"],canCancel=True)
        if option>=2:
            return False

        self.selectedOption=option
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True

        if self.selectedOption==0:
            pass
        elif self.selectedOption==1:
            pass
        return True

class BanishAngelSummon(Effect):
    effType = EFF_TYPE.active

    activateLocation = LOCATION.hand

    AI_HINT = [AI_HINT.eraser]
    AI_POWER = 1
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True
        return True


class minotaur1(Card):
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initMaterialFilter(self.materialFilter,3,3)
        self.initEffect(minotaur_effect1)

    def materialFilter(self,cards:List[Card]):
        if cards[0].race==RACE.UNDEAD and cards[1].race==RACE.BEAST:
            return True

class minotaur_effect1(Effect):
    effType = EFF_TYPE.active

    observeSignals = (LOCATION.monsterZone,[Signal.NormalSummon])

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
        return True



class Dragonide1(Card):
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(Dragonide_effect1)
        pass

class Dragonide_effect1(Effect):
    effType = EFF_TYPE.active

    # observeSignals = (LOCATION.monsterZone,[Signal.BeforeActivateCardEffect])

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 1
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal:Signal.BeforeActivateCardEffect):
        if justCheck:
            return True

        # card=signal.card
        # yield self.y_negativeCard(card)
        yield self.y_destroyCard(self.owner)
        return True



class Manticore1(Card):
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(Manticore_effect1)
        pass

class Manticore_effect1(Effect):
    effType = EFF_TYPE.permanent

    observeSignals = (LOCATION.monsterZone,[Signal.AttachMonsterZone, Signal.DetachMonsterZone])

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 1

    def y_signal(self, signal):
        if isSignal(signal,Signal.AttachMonsterZone):
            if self.owner.isInMonsterZone():
                yield self.y_setBuffEnabled(True)
        elif isSignal(signal,Signal.DetachMonsterZone):
            if signal.card==self.owner: #me leave
                yield self.y_setBuffEnabled(False)
            else: #other leave
                yield self.y_removeBuffEffectSource(signal.card,self.effUniID)


    def y_setBuffEnabled(self,isEnbaled):
        monsterList=self.searchCards(LOCATION.monsterZone,self.getSide(),CARD_TYPE.monster)
        if isEnbaled:
            yield self.y_addCardData(monsterList, 1000, 1000, effDuration=EFF_DURATION.fromSource,
                                     uniqueSourceID=self.effUniID)
        else:
            yield self.y_removeBuffEffectSource(monsterList,self.effUniID)

    def y_effectEnabled(self,isEnabled):
        pass

class maniti_leaveField(Effect):
    effType = EFF_TYPE.trigger

    observeSignals = (LOCATION.monsterZone,[Signal.LeaveField])

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 1
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        if isSignal(signal,Signal.LeaveField,self.owner):
            pass
        else:
            return False

        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True

        TEMP_ERROR("success leave field")
        return True

class mantiti_specialSummon(Effect):
    effType = EFF_TYPE.active

    activateLocation = LOCATION.hand

    AI_HINT = [AI_HINT.summoner]
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
        yield self.y_specialSummon(self.owner)
        return True



class DarkKnight1(Card):
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(DarkKnight_effect1)


class DarkKnight_effect1(Effect):
    effType = EFF_TYPE.active

    observeSignals = (LOCATION.monsterZone,[Signal.NormalSummon])

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
        return True




class Fusion_monster(Card):
    AUTHOR="Unnamed"
    def materialFilter(self,cardList:List[Card]):
        if cardList[0].cardKey=="aaa" and cardList[1].cardKey=="bbb":
            return True
    def effectsInit(self):
        self.initMaterialFilter(self.materialFilter,2)
        self.initEffect(Fusion_monster_effect1)

class Fusion_monster_effect1(Effect):
    effType = EFF_TYPE.active

    observeSignals = (LOCATION.monsterZone,[Signal.NormalSummon])

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 1
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal:Signal.BattleFinish):
        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True
        return True




class LizardWarrior1(Card):
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(LizardWarrior_effect1)

class LizardWarrior_effect1(Effect):
    effType = EFF_TYPE.active

    observeSignals = (LOCATION.monsterZone,[Signal.NormalSummon])

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
        DEBUG_MSG("l effect")
        return True







"""
效果 $${HERO} short


如果是自肃,回合结束前无法召唤等等,就是创建一个新效果,效果有时间限制

"""
class gorgon1(Card):
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(gorgon_effect1)

"""
<场上效果>[丢弃一张手牌]:对方场上一只怪兽的{ATK}下降200
"""
class gorgon_effect1(Effect):
    effType = EFF_TYPE.active

    activateLocation = LOCATION.monsterZone
    # observeSignals = (LOCATION.monsterZone,[Signal.NormalSummon])

    AI_HINT = [AI_HINT.debuff]
    EFF_POWER = 5
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        cards=self.searchCards(LOCATION.hand, self.getSide(), CARD_TYPE.all)
        if not cards:
            return False

        enemyCards=self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster)
        if not enemyCards:
            return False

        if justCheck:
            return True

        card=yield self.y_select1Card(self.getSide(), TITLE.sendToGrave, cards, canCancel=True)
        if not card:
            return False

        successNum=yield self.y_sendCardToGrave(card)
        if not successNum:
            return False

        target=yield self.y_select1Card(self.getSide(),TITLE.target,enemyCards,canCancel=False)
        if not target:
            return False
        self.saveTarget1(target)
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True

        enemyCard=self.getLegalTarget1()
        if not enemyCard:
            return False
        yield self.game.y_addCardData(enemyCard,-200)

        return True




class TestFusion(Card):
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(TestFusion_effect1)

    def materialFilter(self,cardList:List[Card]):
        if len(cardList)==2 and cardList[0].race==RACE.WARRIOR and cardList[1].race==RACE.UNDEAD:
            return True
        return False


class TestFusion_effect1(Effect):
    effType = EFF_TYPE.active

    observeSignals = (LOCATION.monsterZone,[Signal.NormalSummon])

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
        return True


class Dystopia_Soldier_02_effect1(Effect):
    effType = EFF_TYPE.active

    activateLocation = LOCATION.monsterZone
    observeSignals = (LOCATION.monsterZone,[Signal.AttachMonsterZone, Signal.DetachMonsterZone])

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 5
    def y_signal(self,signal):
        if isSignal(signal, Signal.DetachMonsterZone) and signal.card==self.theCard:
            yield self.y_removeBuffWithEffectSource(self.theCard,self)
            self.theCard=None

    def y_cost(self,justCheck:bool,signal):
        # cardList=self.searchCards(LOCATION.monsterZone, 0, CARD_TYPE.monster, self, fitter.filterCanBeDestroy)
        #
        # if len(cardList)==0:
        #     return False

        if justCheck:
            return True

        # theCard=yield self.y_select1Card(self.getSide(), TITLE.destroy, cardList, canCancel=True)
        # if not theCard:
        #     return False
        #
        # self.saveTarget(theCard)
        DEBUG_MSG("this is hello cost")

        return True

    theCard=None
    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True

        DEBUG_MSG("this is hello effect")


    # theCard=self.getLegalTarget()
        # if not theCard:
        #     return False
        # self.theCard=theCard
        # yield self.y_cardDataAdd(theCard, 1, 1, 1, effDuration=EFF_DURATION.fromSource,sourceEffect=self)

        yield self.y_addCardData(self.owner, attackAdd=2)
        return True



class seacrab(Card):
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(seacrab_effect1)

class seacrab_effect1(Effect):
    effType = EFF_TYPE.instant

    observeSignals = (LOCATION.monsterZone, [Signal.NormalSummon])

    AI_HINT=[AI_HINT.permanent]
    EFF_POWER = 0
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal:Signal.Signal):
        if not isSignal(signal,Signal.NormalSummon):
            return False

        if signal.card!=self.owner:
            return False

        if justCheck:
            return True

        return True




class ghoul_boss1(Card):
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(ghoul_boss_effectSummon)

class ghoul_boss_effectSummon(Effect):
    effType = EFF_TYPE.active
    manaCost = 1

    activateLocation = LOCATION.monsterZone

    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 5

    def filter(self,card):
        if card.race!=RACE.UNDEAD:
            return False

        if card.level>4:
            return False

        if not card.canSpecialSummon():
            return False

    def y_activate(self,justCheck:bool,signal:Signal.NormalSummon):
        cardList=self.game.searchCards(LOCATION.hand, self.getSide(), CARD_TYPE.monster, self.filter)

        if not len(cardList):
            return False


        if justCheck:
            return True

        card=yield self.game.y_select1Card(self.getSide(), TITLE.specialSummon, cardList)
        yield self.game.y_specialSummon(card)
        return True

"""
<>
"""


class Berserker(Card):
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(Berserker_effect1)

class Berserker_effect1(Effect):
    effType = EFF_TYPE.trigger

    observeSignals = (LOCATION.monsterZone,[Signal.DestroyedByBattle])

    AI_HINT = [AI_HINT.drawCard,AI_HINT.battleBenefit]
    EFF_POWER = 1

    def y_activate(self,justCheck:bool,signal:Signal.DestroyedByBattle):
        if isSignal(signal,Signal.DestroyedByBattle) and signal.reasonCard==self.owner:
            pass
        else:
            return False

        if justCheck:
            return True

        yield self.y_drawCard(self.getSide())
        return True


class shenyi(Card):
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(shenyi_effect1)

class shenyi_effect1(Effect):
    effType = EFF_TYPE.active

    activateLocation = LOCATION.hand

    specificOperate = OPERATE.activateEffect_specialSummon

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 1
    def y_signal(self,signal):


        pass

    def y_cost(self,justCheck:bool,signal):
        def f(card):
            return card.race==RACE.FAIRY
        mycards=self.searchCards(LOCATION.monsterZone,self.getSide(),CARD_TYPE.monster,None,f)

        if not mycards:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True

        successNum=yield self.y_specialSummon(self.owner)
        if successNum:
            yield self.y_drawCard(self.getSide(),1)
        return True

class shenyi_effect2(Effect):
    effType = EFF_TYPE.permanent

    observeSignals = (LOCATION.monsterZone,[Signal.AttachMonsterZone, Signal.DetachMonsterZone,Signal.CardRaceChanged,Signal.CardLevelChanged])

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 1

    def y_signal(self, signal):
        if isSignal(signal,Signal.DetachMonsterZone):
            if signal.card==self.owner: #me leave
                yield self.y_removeFieldEffectSource()
            else: #other leave
                yield self.y_removeBuffEffectSource(signal.card,self.effUniID)
        else:
            if self.owner.isMonsterOnField():
                yield self.y_recalBuff()


    def fieldFilter(self,card):
        if card.race==RACE.FAIRY and card.level<5:
            return True


    def y_recalBuff(self):
        monsterList=self.searchCards(LOCATION.monsterZone,self.getSide(),CARD_TYPE.monster)
        fairyMonsters=self.searchCards(LOCATION.monsterZone,self.getSide(),CARD_TYPE.monster,None,self.fieldFilter)

        notFairyMonsters=[x for x in monsterList if x not in fairyMonsters]
        yield self.y_addImmunityBuffToCard(fairyMonsters, IMMUNITY_MASK.spell, effDuration=EFF_DURATION.fromSource,
                                     uniqueSourceID=self.effUniID)
        yield self.y_removeBuffEffectSource(notFairyMonsters,self.effUniID)


    def y_removeFieldEffectSource(self):
        monsterList=self.searchCards(LOCATION.monsterZone,self.getSide(),CARD_TYPE.monster)
        yield self.y_removeBuffEffectSource(monsterList,self.effUniID)

class shenyi_effect3(Effect):
    effType = EFF_TYPE.active

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 1

    def y_cost(self,justCheck:bool,signal):
        myMonsters=self.searchCards(LOCATION.monsterZone,self.getSide(),CARD_TYPE.monster)
        cardKeyList=[]
        for monter in myMonsters:
            if monter.getName() not in cardKeyList:
                cardKeyList.append(monter.getName())
        if len(cardKeyList)<3:
            return False


        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True

        enemyMonsters=self.searchCards(LOCATION.monsterZone,self.getEnemySideTuple(),CARD_TYPE.monster,self)
        yield self.y_silenceCard(enemyMonsters)
        yield self.y_multiplyCardData(enemyMonsters,1/2,1/2,effDuration=EFF_DURATION.utilTurnEnds)
        return True


class effectee(Effect):
    effType = EFF_TYPE.active

    activateLocation = LOCATION.monsterZone

    AI_HINT = [AI_HINT.enhance]
    AI_POWER = 1
    def y_signal(self,signal:Signal.TurnEnds):
        pass

    def y_cost(self,justCheck:bool,signal:Signal.BattlePreData):
        if isSignal(signal,Signal.BattlePreData):
            pass

        if justCheck:
            return True

        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True
        return True