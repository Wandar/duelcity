# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Tyrant Dragon
卡名:暴君龙
效果:1T:<召唤时>:破坏对方场上攻击力最高的1只怪兽。
"""

class Wyvern(Card):
    CARD_KEY = "Wyvern"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Wyvern_e1)


class Wyvern_e1(Effect):
    # 1T:<召唤时>:破坏对方场上攻击力最高的1只怪兽。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 4

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        enemies = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self)
        if not enemies:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        enemies = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self)
        if not enemies:
            return False
        best = max(enemies, key=lambda c: c.atk)
        yield self.y_destroyCard(best)
        return True
