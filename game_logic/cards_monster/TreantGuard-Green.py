# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Vineplate Forest Guard
卡名:藤甲守林卫
效果:1A:[丢弃1只植物族怪兽]:发现一张等级3以下的植物族怪兽并特殊召唤。
"""

class TreantGuard_Green(Card):
    CARD_KEY = 'TreantGuard-Green'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(TreantGuard_Green_e1)


class TreantGuard_Green_e1(Effect):
    # 1A:[丢弃1只植物族怪兽]:发现一张等级3以下的植物族怪兽并特殊召唤。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.summoner, AI_HINT.costHand]
    EFF_POWER = 4

    def y_cost(self, justCheck, signal):
        def isR(c):
            return c.race == RACE.PLANT
        fodder = self.searchCards(LOCATION.hand, self.getSide(), CARD_TYPE.monster, self, isR)
        if not fodder:
            return False
        if self.freeMonsterSpace() == 0:
            return False
        if justCheck:
            return True
        cost = yield self.y_select1Card(fodder, TITLE.discard, canCancel=True)
        if not cost:
            return False
        yield self.y_sendCardToGrave(cost)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        if self.freeMonsterSpace() == 0:
            return False
        picked = yield self.y_discoverCard(title=TITLE.specialSummon, side=self.getSide(), race=RACE.PLANT,
                                           cardType=CARD_TYPE.monster, maxLevel=3, count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked)
        return True
