# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Giant Mouth Thorn King
卡名:巨嘴刺王
效果:1T:<召唤时>:发现一张等级3以下的植物族怪兽并沉默召唤。
"""

class Cactus_Boss(Card):
    CARD_KEY = "Cactus Boss"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Cactus_Boss_e1)


class Cactus_Boss_e1(Effect):
    # 1T:<召唤时>:发现一张等级3以下的植物族怪兽并沉默召唤(召唤后无效其效果)。
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
        picked = yield self.y_discoverCard(title=TITLE.specialSummon, side=self.getSide(), race=RACE.PLANT,
                                           cardType=CARD_TYPE.monster, maxLevel=3, count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked)
            if picked.isMonsterOnField():
                yield self.y_silenceCard(picked, effDuration=EFF_DURATION.onceForever)
        return True
