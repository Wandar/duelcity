# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Tiny Stone Golem
卡名:石头小傀儡
效果:1A:[丢弃1只岩石族怪兽]:发现一张等级2以下的岩石族怪兽并守备召唤。
"""

class ms01_Golem_1(Card):
    CARD_KEY = 'ms01_Golem_1'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(ms01_Golem_1_e1)


class ms01_Golem_1_e1(Effect):
    # 1A:[丢弃1只岩石族怪兽]:发现一张等级2以下的岩石族怪兽并守备召唤。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.summoner, AI_HINT.costHand]
    EFF_POWER = 4

    def y_cost(self, justCheck, signal):
        def isR(c):
            return c.race == RACE.ROCK
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
        picked = yield self.y_discoverCard(side=self.getSide(), race=RACE.ROCK,
                                           cardType=CARD_TYPE.monster, maxLevel=2, count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked, form=FORM.defence)
        return True
