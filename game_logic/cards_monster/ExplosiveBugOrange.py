# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Explosive Bug
卡名:爆炸虫
效果:1T:<被破坏后>:对场上所有其他怪兽造成600点伤害。
"""

class ExplosiveBugOrange(Card):
    CARD_KEY = 'ExplosiveBugOrange'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(ExplosiveBugOrange_e1)


class ExplosiveBugOrange_e1(Effect):
    # 1T:<被破坏后>:对场上所有其他怪兽造成600点伤害。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.grave, [Signal.Destroyed])
    AI_HINT = [AI_HINT.damager]
    EFF_POWER = 4

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Destroyed, self.owner):
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        def isOther(c):
            return c != self.owner
        targets = self.searchCards(LOCATION.monsterZone, -1, CARD_TYPE.monster, self, isOther)
        if targets:
            yield self.y_damageCard(targets, 600)
        return True

