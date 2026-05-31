# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_soul_absorption
卡名:灵魂吸收
"""

#########################my

"""
1T:<场上效果>[不限次数]:自己每次有怪兽送去墓地时,回复300基本分
"""

class tT_Card_Ico_soul_absorption(Card):
    CARD_KEY="T_Card_Ico_soul_absorption"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_soul_absorption_effect1)

class tT_Card_Ico_soul_absorption_effect1(Effect):
    effType = EFF_TYPE.trigger

    countLimit = COUNT_LIMIT.unlimited

    observeSignals = (LOCATION.spellTrapZone, [Signal.EnterGrave])

    AI_HINT = [AI_HINT.enhance]
    AI_POWER = 1

    def y_cost(self, justCheck:bool, signal):
        if not isSignal(signal, Signal.EnterGrave):
            return
        if not (signal.card.cardType & CARD_TYPE.monster):
            return
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        yield self.y_healPlayer(self.getSide(), 300)
