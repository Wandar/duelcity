# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Thornshell
卡名:刺壳巨兽
效果:1T:<此卡被特殊召唤时>:发现一张等级3以下的昆虫族怪兽并特殊召唤。
"""

class Beast_1(Card):
    CARD_KEY = 'Beast_1'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Beast_1_e1)


class Beast_1_e1(Effect):
    # 1T:<此卡被特殊召唤时>:发现一张等级3以下的昆虫族怪兽并特殊召唤。
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
        picked = yield self.y_discoverCard(side=self.getSide(), race=RACE.INSECT,
                                           cardType=CARD_TYPE.monster, maxLevel=3, count=3, title=TITLE.specialSummon, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked)
        return True
