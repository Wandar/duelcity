# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Parasaurolophus
卡名:副栉龙
效果:1T:<召唤时>:发现1张等级4以下的恐龙族怪兽卡并特殊召唤。
"""

class Parasaurolophus(Card):
    CARD_KEY = "Parasaurolophus"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Parasaurolophus_e1)


class Parasaurolophus_e1(Effect):
    # 1T:<召唤时>:发现1张等级4以下的恐龙族怪兽卡并特殊召唤。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 4

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        if self.freeMonsterSpace() == 0:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        picked = yield self.y_discoverCard(side=self.getSide(), race=RACE.DINOSAUR,
                                           cardType=CARD_TYPE.monster, maxLevel=4,
                                           count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked)
        return True
