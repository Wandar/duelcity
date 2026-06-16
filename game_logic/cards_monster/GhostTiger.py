# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Soul War Tiger
卡名:灵魂战虎
效果:1T:<召唤时>:把对方场上攻击力低于此卡的怪兽全部变为守备表示。
"""

class GhostTiger(Card):
    CARD_KEY = 'GhostTiger'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(GhostTiger_e1)


class GhostTiger_e1(Effect):
    # 1T:<召唤时>:把对方场上攻击力低于此卡的怪兽全部变为守备表示。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.debuff]
    EFF_POWER = 4

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        myAtk = self.owner.atk
        def weaker(c):
            return c.isFaceUp() and c.atk < myAtk
        targets = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self, weaker)
        if targets:
            yield self.y_changeForm(targets, FORM.defence)
        return True

