# -*- coding: utf-8 -*-
from __future__ import annotations
import random
from annos import *
from KBEDebug import *
from a import Signal, fitter
from b.Card import *
from a.Effect import *
from a.DuelConstants import *
from Constants import *


"""
1A:<墓地效果>[除外此卡]:从卡组发现一只怪兽加入手牌
"""
class banishGraveSummon(Effect):
    effType = EFF_TYPE.active

    activateLocation = LOCATION.grave

    AI_HINT = [AI_HINT.eraser]
    AI_POWER = 1
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        if justCheck:
            return True

        successNum=yield self.y_banishCard(self.owner)
        return successNum!=0

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True

        themonster=yield self.y_discover1CardFromDeck(CARD_TYPE.monster)
        if themonster:
            yield self.y_returnCardToHand(themonster)
        return True


"""
1T:<场上效果><我方回合结束时>:我方手牌不足3张时,抽卡至3张
"""
class AtEndOfTurnDrawCardTo3(Effect):
    effType = EFF_TYPE.trigger

    observeSignals = (LOCATION.monsterZone,[Signal.TurnEnds])

    AI_HINT = [AI_HINT.drawCard]
    EFF_POWER = 1
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal:Signal.TurnEnds):
        game=self.owner.game
        if game.whoseTurn!=self.getSide():
            return False

        handCardNum=len(game.hands[self.getSide()])
        if handCardNum>=3:
            return False

        if justCheck:
            return True

        drawNum=3-handCardNum
        yield self.y_drawCard(self.getSide(),drawNum)

        return True


"""
1A:<场上效果>[从手牌丢弃1只怪兽]:抽1张卡
"""
class Send1MonsterDraw(Effect):
    effType = EFF_TYPE.active

    AI_HINT = [AI_HINT.drawCard]
    EFF_POWER = 1
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        myMonsters=self.searchCards(LOCATION.hand,self.getSide(),CARD_TYPE.monster,self)
        if not myMonsters:
            return False
        if justCheck:
            return True

        monster=yield self.y_select1Card(myMonsters,TITLE.sendToGrave)
        yield self.y_sendCardToGrave(monster)
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True

        yield self.y_drawCard(self.getSide())
        return True



"""
1T:<墓地效果>:此卡被破坏时,将对方墓地一只LV4以下的怪兽加入我方手牌
"""
class DestroyedGetEnemyGraveMonster(Effect):
    effType = EFF_TYPE.trigger

    observeSignals = (LOCATION.grave,[Signal.Destroyed])

    AI_HINT = [AI_HINT.earn]
    EFF_POWER = 2
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal):
        if not isSignal(signal,Signal.Destroyed,self.owner):
            return False

        def f(card):
            return card.level<=4

        enemyGraveMonsters=self.searchCards(LOCATION.grave,self.getEnemySideTuple(),CARD_TYPE.monster,self,f)
        if not enemyGraveMonsters:
            return False
        if justCheck:
            return True

        theCard=yield self.y_select1Card(enemyGraveMonsters,TITLE.addToHand,self.getSide())
        if theCard:
            yield self.y_returnCardToHand(theCard,self.getSide())
        return True


"""
1T:<场上效果>:此卡从场上离开时,从手牌丢弃1只怪兽,然后抽1张卡
"""
class LeaveFieldDiscardDraw(Effect):
    effType = EFF_TYPE.trigger

    observeSignals = (LOCATION.monsterZone,[Signal.LeaveField])

    AI_HINT = [AI_HINT.drawCard]
    EFF_POWER = 2
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        if not isSignal(signal,Signal.LeaveField,self.owner):
            return False

        myHandMonsters=self.searchCards(LOCATION.hand,self.getSide(),CARD_TYPE.monster,self)
        if not myHandMonsters:
            return False
        if justCheck:
            return True

        monster=yield self.y_select1Card(myHandMonsters,TITLE.sendToGrave,self.getSide())
        if not monster:
            return False
        yield self.y_sendCardToGrave(monster)
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True
        yield self.y_drawCard(self.getSide())
        return True


"""
1A:<场上效果>[献祭此卡]:从卡组检索1张魔法卡加入手牌
"""
class TributeSelfSearchSpell(Effect):
    effType = EFF_TYPE.active

    AI_HINT = [AI_HINT.search]
    EFF_POWER = 2
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        if justCheck:
            return True
        successNum=yield self.y_tributeCard(self.owner)
        return successNum!=0

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True
        yield self.y_discover1CardFromDeck(CARD_TYPE.spell)
        return True


"""
1T:<场上效果>:此卡被通常召唤时,从卡组顶检查3张,选1张加入手牌,其余放回卡组下方
"""
class NormalSummonTop3Pick(Effect):
    effType = EFF_TYPE.trigger

    observeSignals = (LOCATION.monsterZone,[Signal.NormalSummon])

    AI_HINT = [AI_HINT.search]
    EFF_POWER = 2
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal):
        if not isSignal(signal,Signal.NormalSummon,self.owner):
            return False

        deckCards=self.game.decks[self.getSide()]
        if not deckCards:
            return False

        if justCheck:
            return True

        pickNum=min(3,len(deckCards))
        top=[]
        for i in range(pickNum):
            top.append(deckCards[len(deckCards)-1-i])

        theCard=yield self.y_select1Card(top,TITLE.addToHand,self.getSide())
        if theCard:
            yield self.y_returnCardToHand(theCard,self.getSide())
            top.remove(theCard)

        for c in top:
            if c in deckCards:
                deckCards.remove(c)
                deckCards.insert(0,c)
        return True


"""
1A:<手牌效果>[将此卡送去墓地]:抽1张卡
"""
class DiscardSelfDraw(Effect):
    effType = EFF_TYPE.active

    activateLocation = LOCATION.hand

    AI_HINT = [AI_HINT.drawCard]
    EFF_POWER = 1
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        if justCheck:
            return True
        successNum=yield self.y_sendCardToGrave(self.owner)
        return successNum!=0

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True
        yield self.y_drawCard(self.getSide())
        return True


"""
1T:<场上效果>:我方准备阶段时,若我方手牌为0,抽1张卡
"""
class StandbyEmptyHandDraw(Effect):
    effType = EFF_TYPE.trigger

    observeSignals = (LOCATION.monsterZone,[Signal.StandbyPhase])

    AI_HINT = [AI_HINT.drawCard]
    EFF_POWER = 2
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal:Signal.StandbyPhase):
        if not isSignal(signal,Signal.StandbyPhase):
            return False
        if self.game.whoseTurn!=self.getSide():
            return False
        if len(self.game.hands[self.getSide()])!=0:
            return False

        if justCheck:
            return True

        yield self.y_drawCard(self.getSide())
        return True


"""
1A:<场上效果>[献祭此卡]:从我方墓地将1只怪兽加入手牌
"""
class TributeSelfReviveToHand(Effect):
    effType = EFF_TYPE.active

    AI_HINT = [AI_HINT.earn]
    EFF_POWER = 2
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        myGraveMonsters=self.searchCards(LOCATION.grave,self.getSide(),CARD_TYPE.monster)
        if not myGraveMonsters:
            return False
        if justCheck:
            return True
        successNum=yield self.y_tributeCard(self.owner)
        return successNum!=0

    def y_activate(self,justCheck:bool,signal):
        myGraveMonsters=self.searchCards(LOCATION.grave,self.getSide(),CARD_TYPE.monster)
        if not myGraveMonsters:
            return False
        if justCheck:
            return True

        theCard=yield self.y_select1Card(myGraveMonsters,TITLE.addToHand,self.getSide())
        if theCard:
            yield self.y_returnCardToHand(theCard,self.getSide())
        return True


"""
1T:<被破坏时>:从卡组检索1只与此卡同种族的怪兽
"""
class DestroyedSearchSameRace(Effect):
    effType = EFF_TYPE.trigger

    observeSignals = (LOCATION.grave,[Signal.Destroyed])

    AI_HINT = [AI_HINT.searchMonster]
    EFF_POWER = 2

    theRace=RACE.none
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal):
        if not isSignal(signal,Signal.Destroyed,self.owner):
            return False

        self.theRace=self.owner.race

        def f(card):
            return card.race==self.theRace

        deckMonsters=self.searchCards(LOCATION.deck,self.getSide(),CARD_TYPE.monster,self,f)
        if not deckMonsters:
            return False
        if justCheck:
            return True

        pickList=deckMonsters
        if len(pickList)>3:
            pickList=random.sample(pickList,3)

        theCard=yield self.y_select1Card(pickList,TITLE.addToHand,self.getSide())
        if theCard:
            yield self.y_returnCardToHand(theCard,self.getSide())
        return True


"""
1A:<场上效果>[从手牌丢弃1张卡]:从卡组顶检查5张,发现1只怪兽加入手牌,其余洗回卡组
"""
class DiscardHandPeek5(Effect):
    effType = EFF_TYPE.active

    AI_HINT = [AI_HINT.searchMonster]
    EFF_POWER = 3
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        myHand=self.searchCards(LOCATION.hand,self.getSide(),CARD_TYPE.all,self)
        if not myHand:
            return False
        if justCheck:
            return True

        theCard=yield self.y_select1Card(myHand,TITLE.sendToGrave,self.getSide())
        if not theCard:
            return False
        yield self.y_sendCardToGrave(theCard)
        return True

    def y_activate(self,justCheck:bool,signal):
        deckCards=self.game.decks[self.getSide()]
        if not deckCards:
            return False
        if justCheck:
            return True

        pickNum=min(5,len(deckCards))
        top=[]
        for i in range(pickNum):
            top.append(deckCards[len(deckCards)-1-i])

        monsters=[c for c in top if c.cardType&CARD_TYPE.monster]
        if monsters:
            theCard=yield self.y_select1Card(monsters,TITLE.addToHand,self.getSide())
            if theCard:
                yield self.y_returnCardToHand(theCard,self.getSide())

        # 剩下的卡已经在卡组里,洗混即可
        random.shuffle(deckCards)
        return True


"""
1T:<场上效果>[不限次数]:对方在抽卡阶段以外抽卡时,抽1张卡
"""
class OppDrawByEffectDraw(Effect):
    effType = EFF_TYPE.trigger

    observeSignals = (LOCATION.monsterZone,[Signal.DrawCardsByEffect])

    countLimit = COUNT_LIMIT.unlimited

    AI_HINT = [AI_HINT.drawCard]
    EFF_POWER = 3
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal:Signal.DrawCardsByEffect):
        if not isSignal(signal,Signal.DrawCardsByEffect):
            return False
        if not signal.sideTuple:
            return False

        enemySides=self.getEnemySideTuple()
        if not any(s in signal.sideTuple for s in enemySides):
            return False

        if justCheck:
            return True

        yield self.y_drawCard(self.getSide())
        return True
