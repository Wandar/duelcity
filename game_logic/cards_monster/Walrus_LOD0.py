# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Polar Pup Walrus
卡名:极地小海象
效果:1A:把自己弃牌区1只水属性怪兽放回自己卡组顶端。
"""

class Walrus_LOD0(Card):
    CARD_KEY = 'Walrus_LOD0'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Walrus_LOD0_e1)


class Walrus_LOD0_e1(Effect):
    # 1A:把自己弃牌区1只水属性怪兽放回自己卡组顶端。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.earn]
    EFF_POWER = 2

    def y_cost(self, justCheck, signal):
        def isWater(c):
            return c.attr == ATTR.WATER
        targets = self.searchCards(LOCATION.grave, self.getSide(), CARD_TYPE.monster, self, isWater)
        if not targets:
            return False
        if justCheck:
            return True
        t = yield self.y_select1Card(targets, TITLE.returnToDeck, canCancel=True)
        if not t:
            return False
        self.saveTarget1(t)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1()
        if not t:
            return False
        yield self.y_returnCardToDeck(t, self.getSide(), RETURN_TO_DECK.top)
        return True

