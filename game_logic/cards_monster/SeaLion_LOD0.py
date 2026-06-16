# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Polar Pup Sea Lion
卡名:极地小海狮
效果:1A:[把自己场上1只其他怪兽返回手牌]:从手牌把1只水属性怪兽特殊召唤。
"""

class SeaLion_LOD0(Card):
    CARD_KEY = 'SeaLion_LOD0'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(SeaLion_LOD0_e1)


class SeaLion_LOD0_e1(Effect):
    # 1A:[把自己场上1只其他怪兽返回手牌]:从手牌把1只水属性怪兽特殊召唤。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        def isOther(c):
            return c != self.owner
        fodder = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self, isOther)
        if not fodder:
            return False
        def isWater(c):
            return c.attr == ATTR.WATER
        handTargets = self.searchCards(LOCATION.hand, self.getSide(), CARD_TYPE.monster, self, isWater)
        if not handTargets:
            return False
        if justCheck:
            return True
        cost = yield self.y_select1Card(fodder, TITLE.returnToHand, canCancel=True)
        if not cost:
            return False
        summon = yield self.y_select1Card(handTargets, TITLE.specialSummon, canCancel=True)
        if not summon:
            return False
        yield self.y_returnCardToHand(cost)
        self.saveTarget1(summon)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1()
        if not t:
            return False
        if self.freeMonsterSpace() == 0:
            return False
        yield self.y_specialSummon(t)
        return True

