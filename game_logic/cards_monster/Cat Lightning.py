# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:yellow Lightning Cat
卡名:黄闪电猫
效果:1T:<召唤时>:从手牌把1只「红闪电猫」特殊召唤。
"""

class Cat_Lightning(Card):
    CARD_KEY = 'Cat Lightning'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Cat_Lightning_e1)


class Cat_Lightning_e1(Effect):
    # 1T:<召唤时>:从手牌把1只「红闪电猫」特殊召唤。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        def isTarget(c):
            return c.cardKey == "Cat Bolt"
        targets = self.searchCards(LOCATION.hand, self.getSide(), CARD_TYPE.monster, self, isTarget)
        if not targets:
            return False
        if self.freeMonsterSpace() == 0:
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
        yield self.y_specialSummon(t)
        return True

