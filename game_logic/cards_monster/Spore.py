# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Spore Orb
卡名:孢子球
效果:1T:<此卡被特殊召唤时>:发现一张等级2以下的植物族怪兽并守备召唤。
"""

class Spore(Card):
    CARD_KEY = "Spore"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Spore_e1)


class Spore_e1(Effect):
    # 1T:<此卡被特殊召唤时>:发现一张等级2以下的植物族怪兽并守备召唤。
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
        picked = yield self.y_discoverCard(side=self.getSide(), race=RACE.PLANT,
                                           cardType=CARD_TYPE.monster, maxLevel=2, count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked, form=FORM.defence)
        return True
