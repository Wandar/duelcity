# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Woodland Wyrm
卡名:森林妖龙
效果:1T:<墓地效果:自己的植物族怪兽被破坏时>:把此卡特殊召唤。
"""

class ForestDrake_Blue(Card):
    CARD_KEY = 'ForestDrake_Blue'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(ForestDrake_Blue_e1)


class ForestDrake_Blue_e1(Effect):
    # 1T:<墓地效果:自己的植物族怪兽被破坏时>:把此卡特殊召唤。
    effType = EFF_TYPE.optionalTrigger
    observeSignals = (LOCATION.grave, [Signal.Destroyed])
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Destroyed):
            return False
        if self.owner.location != LOCATION.grave:
            return False
        card = signal.card
        if card is None or card == self.owner:
            return False
        if card.side != self.getSide() or card.race != RACE.PLANT:
            return False
        if self.freeMonsterSpace() == 0:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        yield self.y_specialSummon(self.owner)
        return True

