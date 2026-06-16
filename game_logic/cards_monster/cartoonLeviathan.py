# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Tiny Green Dragon
卡名:小绿龙
效果:1T:<被破坏后>:自己回复800基本分。
"""

class cartoonLeviathan(Card):
    CARD_KEY = 'cartoonLeviathan'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(cartoonLeviathan_e1)


class cartoonLeviathan_e1(Effect):
    # 1T:<被破坏后>:自己回复800基本分。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.grave, [Signal.Destroyed])
    AI_HINT = [AI_HINT.recoverLP]
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
        yield self.y_healPlayer(self.getSide(), 800)
        return True

