# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Tiny Bee
卡名:小蜜蜂
效果:1T:<被破坏后>:发现1张LV4以下的昆虫族怪兽卡。
"""

class ms03_Bee_1(Card):
    CARD_KEY = 'ms03_Bee_1'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(ms03_Bee_1_e1)


class ms03_Bee_1_e1(Effect):
    # 1T:<被破坏后>:发现1张LV4以下的昆虫族怪兽卡。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.grave, [Signal.Destroyed])
    AI_HINT = [AI_HINT.searchMonster]
    EFF_POWER = 2

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Destroyed, self.owner):
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        yield self.y_discoverCard(side=self.getSide(), race=RACE.INSECT,
                                  cardType=CARD_TYPE.monster, maxLevel=4, count=3, canCancel=True)
        return True

