# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:yellow Lightning Cat
卡名:黄闪电猫
效果:1A:[丢弃1只兽族怪兽]:发现一张等级2以下的兽族怪兽并守备召唤。
"""

class Cat_Lightning(Card):
    CARD_KEY = "Cat Lightning"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Cat_Lightning_e1)


class Cat_Lightning_e1(Effect):
    # 1A:[丢弃1只兽族怪兽]:发现一张等级2以下的兽族怪兽并守备召唤。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.summoner, AI_HINT.costHand]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        def isBeast(c):
            return c.race == RACE.BEAST
        fodder = self.searchCards(LOCATION.hand, self.getSide(), CARD_TYPE.monster, self, isBeast)
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
        picked = yield self.y_discoverCard(title=TITLE.specialSummon, side=self.getSide(), race=RACE.BEAST,
                                           cardType=CARD_TYPE.monster, maxLevel=2, count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked, form=FORM.defence)
        return True
