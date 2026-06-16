# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Red Lightning Cat
卡名:红闪电猫
效果:1T:<召唤时>:从卡组把1只「黄闪电猫」加入手牌。
"""

class Cat_Bolt(Card):
    CARD_KEY = 'Cat Bolt'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Cat_Bolt_e1)


class Cat_Bolt_e1(Effect):
    # 1T:<召唤时>:从卡组把1只「黄闪电猫」加入手牌。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.searchMonster]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        def isTarget(c):
            return c.cardKey == "Cat Lightning"
        targets = self.searchCards(LOCATION.deck, self.getSide(), CARD_TYPE.monster, self, isTarget)
        if not targets:
            return False
        if justCheck:
            return True
        self.saveTarget1(targets[0])
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1()
        if not t:
            return False
        yield self.y_returnCardToHand(t)
        return True

