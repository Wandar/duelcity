# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Nimble Drakonoid
卡名:灵巧机龙
效果:1A:[把1张手牌送入弃牌区]:发现一张等级4以下的机械族怪兽并特殊召唤。
"""

class Dragon_Bot(Card):
    CARD_KEY = "Dragon Bot"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Dragon_Bot_e1)


class Dragon_Bot_e1(Effect):
    # 1A:[把1张手牌送入弃牌区]:发现一张等级4以下的机械族怪兽并特殊召唤。
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
        picked = yield self.y_discoverCard(title=TITLE.specialSummon, side=self.getSide(), race=RACE.MACHINE,
                                           cardType=CARD_TYPE.monster, maxLevel=4, count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked)
        return True
