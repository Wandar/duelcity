# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Gilded Mechbone Dragon
卡名:黄金机骸龙
效果:1T:<被破坏送入弃牌区时>:从弃牌区把1只机械族或龙族怪兽特殊召唤。
"""

class Dragon7_basemesh1(Card):
    CARD_KEY = 'Dragon7_basemesh1'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Dragon7_basemesh1_e1)


class Dragon7_basemesh1_e1(Effect):
    # 1T:<被破坏送入弃牌区时>:从弃牌区把1只机械族或龙族怪兽特殊召唤。
    effType = EFF_TYPE.optionalTrigger
    observeSignals = (LOCATION.grave, [Signal.Destroyed])
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 4

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Destroyed, self.owner):
            return False
        if self.owner.location != LOCATION.grave:
            return False
        def isTarget(c):
            return c != self.owner and c.race in (RACE.MACHINE, RACE.DRAGON)
        targets = self.searchCards(LOCATION.grave, self.getSide(), CARD_TYPE.monster, self, isTarget)
        if not targets:
            return False
        if self.freeMonsterSpace() == 0:
            return False
        if justCheck:
            return True
        chosen = yield self.y_select1Card(targets, TITLE.specialSummon, canCancel=True)
        if not chosen:
            return False
        self.saveTarget1(chosen)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1(checkLocationChange=False)
        if not t:
            return False
        yield self.y_specialSummon(t)
        return True

