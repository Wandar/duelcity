# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Stump Monster
卡名:树桩怪
效果:1T:<被破坏后>:从卡组把1只等级1的植物族怪兽特殊召唤。
"""

class ms02_Stump_1(Card):
    CARD_KEY = 'ms02_Stump_1'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(ms02_Stump_1_e1)


class ms02_Stump_1_e1(Effect):
    # 1T:<被破坏后>:从卡组把1只等级1的植物族怪兽特殊召唤。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.grave, [Signal.Destroyed])
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Destroyed, self.owner):
            return False
        def isTarget(c):
            return c.race == RACE.PLANT and c.level == 1
        targets = self.searchCards(LOCATION.deck, self.getSide(), CARD_TYPE.monster, self, isTarget)
        if not targets:
            return False
        if self.freeMonsterSpace() == 0:
            return False
        if justCheck:
            return True
        chosen = yield self.y_select1Card(targets, TITLE.specialSummon, canCancel=True)
        if not chosen:
            return False
        self.saveTarget1(chosen)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1(checkLocationChange=False)
        if not t:
            return False
        yield self.y_specialSummon(t)
        return True

