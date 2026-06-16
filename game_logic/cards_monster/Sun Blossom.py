# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Sunlit Winged Sunflower Pixie
卡名:向阳翼花小妖
效果:1T:<被破坏后>:从卡组把1只「向阳翼花妖」特殊召唤。
"""

class Sun_Blossom(Card):
    CARD_KEY = 'Sun Blossom'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Sun_Blossom_e1)


class Sun_Blossom_e1(Effect):
    # 1T:<被破坏后>:从卡组把1只「向阳翼花妖」特殊召唤。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.grave, [Signal.Destroyed])
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Destroyed, self.owner):
            return False
        def isTarget(c):
            return c.cardKey == "Sunflower Fairy"
        targets = self.searchCards(LOCATION.deck, self.getSide(), CARD_TYPE.monster, self, isTarget)
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
        t = self.getLegalTarget1(checkLocationChange=False)
        if not t:
            return False
        yield self.y_specialSummon(t)
        return True

