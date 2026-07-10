# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Salvage Droid
卡名:回收机兵
effect:
效果:1T:<被破坏后>:发现1张机械族怪兽卡并特殊召唤。
"""

class droid(Card):
    CARD_KEY = "droid"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(droid_e1)


class droid_e1(Effect):
    # 1T:<被破坏后>:发现1张机械族怪兽卡并特殊召唤。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.grave, [Signal.Destroyed])
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Destroyed, self.owner):
            return False
        if self.freeMonsterSpace() == 0:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        picked = yield self.y_discoverCard(title=TITLE.specialSummon, side=self.getSide(), race=RACE.MACHINE,
                                           cardType=CARD_TYPE.monster, count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked)
        return True
