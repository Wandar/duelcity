# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Letalobrach
卡名:致命臂龙
"""

class letalobrach(Card):
    CARD_KEY = "letalobrach"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(letalobrach_VitalBond)
        self.initEffect(letalobrach_FatalBackfire)



"""
1A:<墓地效果>:这张卡召唤·反转召唤·特殊召唤成功时，自己回复1000基本分。这张卡被破坏送去墓地时，自己受到2000点伤害。
1T:<When summoned>: Gain 1000 LP.
1T:<When destroyed>: Take 2000 damage.
"""
class letalobrach_VitalBond(Effect):
    effType = EFF_TYPE.trigger

    observeSignals = (LOCATION.monsterZone, [Signal.Summon])

    AI_HINT = [AI_HINT.recoverLP]
    EFF_POWER = 1

    def y_cost(self, justCheck: bool, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        if signal.card != self.owner:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck:
            return True
        yield self.y_healPlayer(self.getSide(), 1000)
        return True


"""
1T:<被破坏时>:你受到2000点伤害。
1T:<When destroyed>: Take 2000 damage.
"""
class letalobrach_FatalBackfire(Effect):
    effType = EFF_TYPE.trigger

    observeSignals = (LOCATION.grave, [Signal.Destroyed])

    AI_HINT = [AI_HINT.damager]
    EFF_POWER = -3

    def y_cost(self, justCheck: bool, signal):
        if not isSignal(signal, Signal.Destroyed, self.owner):
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck:
            return True
        yield self.y_damagePlayer(self.getSide(), 2000)
        return True
