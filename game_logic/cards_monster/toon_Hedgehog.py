# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Rolling Hedgehog
卡名:滚滚刺猬
效果:1T:<召唤时>:发现一张等级4以下的兽族怪兽并特殊召唤。
"""

class toon_Hedgehog(Card):
    CARD_KEY = "toon_Hedgehog"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(toon_Hedgehog_e1)


class toon_Hedgehog_e1(Effect):
    # 1T:<召唤时>:发现一张等级4以下的兽族怪兽并特殊召唤。
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
        picked = yield self.y_discoverCard(title=TITLE.specialSummon, side=self.getSide(), race=RACE.BEAST,
                                           cardType=CARD_TYPE.monster, maxLevel=4, count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked)
        return True
