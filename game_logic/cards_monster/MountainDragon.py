# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Terrabrown Horned Dragon
卡名:地褐角龙
"""

class MountainDragon(Card):
    CARD_KEY = "MountainDragon"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(MountainDragon_AvalancheBreath)


"""
1T:<场上效果>:此卡被召唤成功时,对对手场上所有怪兽各造成500点伤害。
1T:<When this card is Summoned>:Deal 500 damage to all monsters on your opponent's field.
"""
class MountainDragon_AvalancheBreath(Effect):
    effType = EFF_TYPE.trigger

    observeSignals = (LOCATION.monsterZone, [Signal.Summon])

    AI_HINT = [AI_HINT.damager, AI_HINT.eraser]
    EFF_POWER = 3

    def y_cost(self, justCheck: bool, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False

        enemies = self.searchCards(
            LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self
        )
        if not enemies:
            return False

        if justCheck:
            return True
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck:
            return True

        enemies = self.searchCards(
            LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self
        )
        if enemies:
            yield self.y_damageCard(enemies, 500)
        return True
