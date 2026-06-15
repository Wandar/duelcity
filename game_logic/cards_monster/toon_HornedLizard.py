# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Pointy Horned Lizard
卡名:尖尖角蜥
"""

class toon_HornedLizard(Card):
    CARD_KEY="toon_HornedLizard"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(toon_HornedLizard_e1)


"""
1T:<召唤时>:对对方场上所有守备表示的怪兽各造成300点伤害。
"""
class toon_HornedLizard_e1(Effect):
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.damager]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True

        def isDef(c):
            return c.isDefence()

        targets = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(),
                                   CARD_TYPE.monster, self, isDef)
        if targets:
            yield self.y_damageCard(targets, 300)
        return True
