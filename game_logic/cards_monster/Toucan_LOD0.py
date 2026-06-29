# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Toucan
卡名:巨嘴鸟
效果:1A:[丢弃1只鸟兽族怪兽]:发现一张等级2以下的鸟兽族怪兽并守备召唤。
"""

class Toucan_LOD0(Card):
    CARD_KEY = "Toucan_LOD0"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Toucan_LOD0_e1)


class Toucan_LOD0_e1(Effect):
    # 1A:[丢弃1只鸟兽族怪兽]:发现一张等级2以下的鸟兽族怪兽并守备召唤。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.summoner, AI_HINT.costHand]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        def isWindbeast(c):
            return c.race == RACE.WINDBEAST
        fodder = self.searchCards(LOCATION.hand, self.getSide(), CARD_TYPE.monster, self, isWindbeast)
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
        picked = yield self.y_discoverCard(side=self.getSide(), race=RACE.WINDBEAST,
                                           cardType=CARD_TYPE.monster, maxLevel=2, count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked, form=FORM.defence)
        return True
