# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Big-Eared Mouse Archer
卡名:大耳鼠射手
效果:1A:[把1只其他怪兽解放]:发现一张等级2以下的兽战士族怪兽并特殊召唤。
"""

class ms06_Rat_1(Card):
    CARD_KEY = 'ms06_Rat_1'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(ms06_Rat_1_e1)


class ms06_Rat_1_e1(Effect):
    # 1A:[把1只其他怪兽解放]:发现一张等级2以下的兽战士族怪兽并特殊召唤。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.summoner, AI_HINT.costMonster]
    EFF_POWER = 4

    def y_cost(self, justCheck, signal):
        def isOther(c):
            return c != self.owner
        fodder = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self, isOther)
        if not fodder:
            return False
        if justCheck:
            return True
        cost = yield self.y_select1Card(fodder, TITLE.tribute, canCancel=True)
        if not cost:
            return False
        successNum = yield self.y_tributeCard(cost)
        if not successNum:
            return False
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        if self.freeMonsterSpace() == 0:
            return False
        picked = yield self.y_discoverCard(title=TITLE.specialSummon, side=self.getSide(), race=RACE.BEASTWARRIOR,
                                           cardType=CARD_TYPE.monster, maxLevel=2, count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked)
        return True
