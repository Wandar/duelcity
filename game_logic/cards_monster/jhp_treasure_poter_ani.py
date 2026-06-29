# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Treasure Seeker Squirrel
卡名:宝藏搜寻者
效果:1T:<召唤时>:发现一张等级3以下的兽族怪兽并沉默召唤。
"""

class jhp_treasure_poter_ani(Card):
    CARD_KEY = 'jhp_treasure_poter_ani'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(jhp_treasure_poter_ani_e1)


class jhp_treasure_poter_ani_e1(Effect):
    # 1T:<召唤时>:发现一张等级3以下的兽族怪兽并沉默召唤。
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
        picked = yield self.y_discoverCard(side=self.getSide(), race=RACE.BEAST,
                                           cardType=CARD_TYPE.monster, maxLevel=3, count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked)
            if picked.isMonsterOnField():
                yield self.y_silenceCard(picked, effDuration=EFF_DURATION.onceForever)
        return True
