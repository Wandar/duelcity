# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Summer Treant
卡名:夏日树妖
效果:1T:自己的准备阶段:此卡防御力+200。2T:<被破坏后>:从卡组把1只等级2以下的植物族怪兽加入手牌。
"""

class Treant_Summer(Card):
    CARD_KEY = 'Treant_Summer'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Treant_Summer_e1)
        self.initEffect(Treant_Summer_e2)


class Treant_Summer_e1(Effect):
    # 1T:自己的准备阶段:此卡防御力+200。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.StandbyPhase])
    AI_HINT = [AI_HINT.enhance]
    EFF_POWER = 1
    countLimit = COUNT_LIMIT.unlimited

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.StandbyPhase):
            return False
        if self.game.whoseTurn != self.getSide():
            return False
        if not self.owner.isMonsterOnField():
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        yield self.y_addCardData(self.owner, defenceAdd=200, effDuration=EFF_DURATION.onceForever)
        return True


class Treant_Summer_e2(Effect):
    # 2T:<被破坏后>:从卡组把1只等级2以下的植物族怪兽加入手牌。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.grave, [Signal.Destroyed])
    AI_HINT = [AI_HINT.searchMonster]
    EFF_POWER = 2

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Destroyed, self.owner):
            return False
        def isT(c):
            return c.race == RACE.PLANT and c.level <= 2
        targets = self.searchCards(LOCATION.deck, self.getSide(), CARD_TYPE.monster, self, isT)
        if not targets:
            return False
        if justCheck:
            return True
        chosen = yield self.y_select1Card(targets, TITLE.addToHand, canCancel=True)
        if not chosen:
            return False
        self.saveTarget1(chosen)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1()
        if not t:
            return False
        yield self.y_returnCardToHand(t)
        return True

