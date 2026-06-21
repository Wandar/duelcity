# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Luminous Wing
卡名:萤光舞翼
效果:1T:<召唤时>:发现1张攻击力1500以下的昆虫族怪兽卡并特殊召唤。
"""

class GiantBeetle(Card):
    CARD_KEY = "GiantBeetle"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(GiantBeetle_e1)


class GiantBeetle_e1(Effect):
    # 1T:<召唤时>:发现1张攻击力1500以下的昆虫族怪兽卡并特殊召唤。
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
        picked = yield self.y_discoverCard(side=self.getSide(), race=RACE.INSECT,
                                           cardType=CARD_TYPE.monster, maxAtk=1500,
                                           count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked)
        return True
