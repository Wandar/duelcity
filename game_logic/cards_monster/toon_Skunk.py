# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Naughty Skunk
卡名:坏坏臭鼬
"""

class toon_Skunk(Card):
    CARD_KEY="toon_Skunk"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(toon_Skunk_e1)


"""
1T:<被战斗破坏后>:破坏此卡的怪兽返回持有者手牌。
"""
class toon_Skunk_e1(Effect):
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.grave, [Signal.DestroyedByBattle])
    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.DestroyedByBattle, self.owner):
            return False
        killer = signal.reasonCard
        if killer is None:
            return False
        if justCheck:
            return True
        self.saveTarget1(killer)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        target = self.getLegalTarget1(checkLocationChange=False)
        if not target:
            return False
        yield self.y_returnCardToHand(target)
        return True
