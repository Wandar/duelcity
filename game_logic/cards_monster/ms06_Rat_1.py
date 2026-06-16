# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Big-Eared Mouse Archer
卡名:大耳鼠射手
效果:1T:<召唤时>:对对方场上1只怪兽造成300点伤害。
"""

class ms06_Rat_1(Card):
    CARD_KEY = 'ms06_Rat_1'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(ms06_Rat_1_e1)


class ms06_Rat_1_e1(Effect):
    # 1T:<召唤时>:对对方场上1只怪兽造成300点伤害。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.damager]
    EFF_POWER = 2

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        enemies = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self)
        if not enemies:
            return False
        if justCheck:
            return True
        t = yield self.y_select1Card(enemies, TITLE.damage, canCancel=True)
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
        yield self.y_damageCard(t, 300)
        return True

