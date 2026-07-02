# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Sunlit Winged Sunflower Fairy
卡名:向阳翼花妖
效果:1T:<召唤时>:发现一张等级3以下的植物族怪兽并守备召唤。
"""

class Sunflower_Fairy(Card):
    CARD_KEY = "Sunflower Fairy"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Sunflower_Fairy_e1)


class Sunflower_Fairy_e1(Effect):
    # 1T:<召唤时>:发现一张等级3以下的植物族怪兽并守备召唤。
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
            yield self.y_specialSummon(picked, form=FORM.defence)
        return True
