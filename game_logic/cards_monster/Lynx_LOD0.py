# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Spotted Lynx
卡名:斑斑猞猁
效果:1A:[把1只我方怪兽返回手牌]:发现一张等级3以下的兽族怪兽并特殊召唤。
"""

class Lynx_LOD0(Card):
    CARD_KEY = "Lynx_LOD0"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Lynx_LOD0_e1)


class Lynx_LOD0_e1(Effect):
    # 1A:[把1只我方怪兽返回手牌]:发现一张等级3以下的兽族怪兽并特殊召唤。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.summoner, AI_HINT.costMonster]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        mine = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self)
        if not mine:
            return False
        if justCheck:
            return True
        cost = yield self.y_select1Card(mine, TITLE.returnToHand, canCancel=True)
        if not cost:
            return False
        yield self.y_returnCardToHand(cost)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        if self.freeMonsterSpace() == 0:
            return False
        picked = yield self.y_discoverCard(title=TITLE.specialSummon, side=self.getSide(), race=RACE.BEAST,
                                           cardType=CARD_TYPE.monster, maxLevel=3, count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked)
        return True
