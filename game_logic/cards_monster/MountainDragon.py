# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Terrabrown Horned Dragon
卡名:地褐角龙
效果:1T:<召唤时>:破坏对方场上1只守备表示的怪兽。
"""

class MountainDragon(Card):
    CARD_KEY = "MountainDragon"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(MountainDragon_e1)


class MountainDragon_e1(Effect):
    # 1T:<召唤时>:破坏对方场上1只守备表示的怪兽。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        def isDefence(c):
            return c.form in (FORM.defence, FORM.defenceSet)
        targets = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self, isDefence)
        if not targets:
            return False
        if justCheck:
            return True
        t = yield self.y_select1Card(targets, TITLE.destroy, canCancel=True)
        if not t:
            return False
        self.saveTarget1(t)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1()
        if not t:
            return False
        yield self.y_destroyCard(t)
        return True
