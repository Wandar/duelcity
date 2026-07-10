# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Breeze Sprite
卡名:微风精灵
效果:1T:<召唤时>:发现一张等级2以下的天使族怪兽并特殊召唤。
"""

class tinyWind(Card):
    CARD_KEY = 'tinyWind'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(tinyWind_e1)


class tinyWind_e1(Effect):
    # 1T:<召唤时>:发现一张等级2以下的天使族怪兽并特殊召唤。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 3

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
        picked = yield self.y_discoverCard(title=TITLE.specialSummon, side=self.getSide(), race=RACE.FAIRY,
                                           cardType=CARD_TYPE.monster, maxLevel=2, count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked)
        return True
