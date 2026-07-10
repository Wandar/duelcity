# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Departure Goat
卡名:启程山羊
效果:1T:<此卡被特殊召唤时>:发现一张等级2以下的兽族怪兽并特殊召唤。
"""

class Goat_LOD0(Card):
    CARD_KEY = "Goat_LOD0"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Goat_LOD0_e1)


class Goat_LOD0_e1(Effect):
    # 1T:<此卡被特殊召唤时>:发现一张等级2以下的兽族怪兽并特殊召唤。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.SpecialSummon])
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 4

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.SpecialSummon, self.owner):
            return False
        if self.freeMonsterSpace() == 0:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        picked = yield self.y_discoverCard(side=self.getSide(), race=RACE.BEAST,
                                           cardType=CARD_TYPE.monster, maxLevel=2, count=3, title=TITLE.specialSummon, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked)
        return True
