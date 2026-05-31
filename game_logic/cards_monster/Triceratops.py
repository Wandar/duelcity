# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Triceratops
卡名:三角龙
"""

class Triceratops(Card):
    CARD_KEY = "Triceratops"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Triceratops_NatureBlessing)
        self.initEffect(Triceratops_FallenCurse)


"""
1T:<场上效果>:这张卡召唤成功时,自己回复1000基本分。2T:<墓地效果>:这张卡被破坏送去墓地时,自己受到2000点伤害。
1T:<FieldEffect>:When this card is summoned, recover 1000 LP.2T:<GraveEffect>:When this card is destroyed and sent to the Graveyard, take 2000 damage.
"""
class Triceratops_NatureBlessing(Effect):
    effType = EFF_TYPE.trigger

    observeSignals = (LOCATION.monsterZone, [Signal.Summon])

    AI_HINT = [AI_HINT.recoverLP]
    EFF_POWER = 2

    def y_cost(self, justCheck: bool, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
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
1T: <被破坏时,>:你受到2000点伤害。
"""
class Triceratops_FallenCurse(Effect):
    effType = EFF_TYPE.trigger

    observeSignals = (LOCATION.grave, [Signal.Destroyed])

    AI_HINT = [AI_HINT.damager]
    EFF_POWER = -2

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
