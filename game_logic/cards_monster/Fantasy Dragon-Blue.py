# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Storm Wyvern
卡名:风暴亚龙
效果:1A:[丢弃1张手牌]:发现一张等级3以下的龙族怪兽并守备召唤。
"""

class Fantasy_Dragon_Blue(Card):
    CARD_KEY = 'Fantasy Dragon-Blue'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Fantasy_Dragon_Blue_e1)


class Fantasy_Dragon_Blue_e1(Effect):
    # 1A:[丢弃1张手牌]:发现一张等级3以下的龙族怪兽并守备召唤。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.summoner, AI_HINT.costHand]
    EFF_POWER = 4

    def y_cost(self, justCheck, signal):
        hand = self.searchCards(LOCATION.hand, self.getSide(), CARD_TYPE.all, self)
        if not hand:
            return False
        if self.freeMonsterSpace() == 0:
            return False
        if justCheck:
            return True
        cost = yield self.y_select1Card(hand, TITLE.discard, canCancel=True)
        if not cost:
            return False
        yield self.y_sendCardToGrave(cost)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        if self.freeMonsterSpace() == 0:
            return False
        picked = yield self.y_discoverCard(side=self.getSide(), race=RACE.DRAGON,
                                           cardType=CARD_TYPE.monster, maxLevel=3, count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked, form=FORM.defence)
        return True
