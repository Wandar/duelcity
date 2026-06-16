# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Abyssal Blue Drake
卡名:渊蓝龙人
效果:1A:[把此卡解放]:从卡组把1只等级4以下的水属性怪兽特殊召唤。
"""

class Drake_Skinny(Card):
    CARD_KEY = 'Drake Skinny'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Drake_Skinny_e1)


class Drake_Skinny_e1(Effect):
    # 1A:[把此卡解放]:从卡组把1只等级4以下的水属性怪兽特殊召唤。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        def isTarget(c):
            return c.attr == ATTR.WATER and c.level <= 4
        targets = self.searchCards(LOCATION.deck, self.getSide(), CARD_TYPE.monster, self, isTarget)
        if not targets:
            return False
        if justCheck:
            return True
        chosen = yield self.y_select1Card(targets, TITLE.specialSummon, canCancel=True)
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
        t = self.getLegalTarget1(checkLocationChange=False)
        if not t or self.freeMonsterSpace() == 0:
            return False
        yield self.y_specialSummon(t)
        return True

