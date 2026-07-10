# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Bramble Rampage Tusker
卡名:棘丛暴獠
效果:1T:<召唤时>:发现一张等级2以下的兽族怪兽并特殊召唤。
"""

class Bizun_2(Card):
    CARD_KEY = 'Bizun_2'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Bizun_2_e1)


class Bizun_2_e1(Effect):
    # 1T:<召唤时>:发现一张等级2以下的兽族怪兽并特殊召唤。
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
                                           cardType=CARD_TYPE.monster, maxLevel=2, count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked)
        return True
