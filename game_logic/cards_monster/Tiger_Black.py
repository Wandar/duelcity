# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Shadow Tiger
卡名:暗影虎
效果:1A:[把1只我方怪兽返回手牌]:发现一张等级2以下的兽族怪兽并特殊召唤。
"""

class Tiger_Black(Card):
    CARD_KEY = 'Tiger_Black'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Tiger_Black_e1)


class Tiger_Black_e1(Effect):
    # 1A:[把1只我方怪兽返回手牌]:发现一张等级2以下的兽族怪兽并特殊召唤。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.summoner, AI_HINT.costMonster]
    EFF_POWER = 4

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
                                           cardType=CARD_TYPE.monster, maxLevel=2, count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked)
        return True
