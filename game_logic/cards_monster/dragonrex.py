# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Dragonrex
卡名:恐暴龙
效果:1T:<召唤时>:破坏自己场上此卡以外所有怪兽。
"""

class dragonrex(Card):
    CARD_KEY = 'dragonrex'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(dragonrex_e1)


class dragonrex_e1(Effect):
    # 1T:<召唤时>:破坏自己场上此卡以外所有怪兽。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.eraser, AI_HINT.costMonster]
    EFF_POWER = 2

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        def isOther(c):
            return c != self.owner
        targets = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self, isOther)
        if not targets:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        def isOther(c):
            return c != self.owner
        targets = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self, isOther)
        if targets:
            yield self.y_destroyCard(list(targets))
        return True


