# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Ptooey Llama
卡名:呸呸羊驼
效果:1T:<召唤时>:发现一张等级3以下的兽族怪兽并守备召唤。
"""

class Llama_LOD0(Card):
    CARD_KEY = "Llama_LOD0"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Llama_LOD0_e1)


class Llama_LOD0_e1(Effect):
    # 1T:<召唤时>:发现一张等级3以下的兽族怪兽并守备召唤。
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
            yield self.y_specialSummon(picked, form=FORM.defence)
        return True
