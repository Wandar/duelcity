# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Azure Crystal Carapace
卡名:蓝晶甲壳兽
效果:1A:[把此卡解放]:从卡组把2只等级2以下的水属性怪兽特殊召唤。
"""

class StoneBeast(Card):
    CARD_KEY = 'StoneBeast'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(StoneBeast_e1)


class StoneBeast_e1(Effect):
    # 1A:[把此卡解放]:从卡组把2只等级2以下的水属性怪兽特殊召唤。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 4

    def y_cost(self, justCheck, signal):
        def isTarget(c):
            return c.attr == ATTR.WATER and c.level <= 2
        targets = self.searchCards(LOCATION.deck, self.getSide(), CARD_TYPE.monster, self, isTarget)
        if not targets:
            return False
        if justCheck:
            return True
        maxn = min(2, len(targets))
        chosen = yield self.y_selectCards(targets, TITLE.specialSummon, self.getSide(), 1, maxn, None, True)
        if not chosen:
            return False
        successNum = yield self.y_tributeCard(self.owner)
        if not successNum:
            return False
        self.saveTarget1(chosen)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        targets = self.getLegalTarget1(checkLocationChange=False)
        if not targets:
            return False
        if type(targets) != list:
            targets = [targets]
        yield self.y_specialSummon(targets)
        return True

