# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Scarlet-Maned Autumn Giant
卡名:红鬃秋巨人
效果:1A:[丢弃1张手牌]:发现一张等级4以下的恶魔族怪兽并特殊召唤。2A:[丢弃1张手牌]:从卡组检索1只恶魔族怪兽并覆盖。
"""

class Giant_Autumn(Card):
    CARD_KEY = "Giant_Autumn"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Giant_Autumn_e1)
        self.initEffect(Giant_Autumn_e2)


class Giant_Autumn_e1(Effect):
    # 1A:[丢弃1张手牌]:发现一张等级4以下的恶魔族怪兽并特殊召唤。
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
        picked = yield self.y_discoverCard(side=self.getSide(), race=RACE.FIEND,
                                           cardType=CARD_TYPE.monster, maxLevel=4, count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked)
        return True


class Giant_Autumn_e2(Effect):
    # 2A:[丢弃1张手牌]:从卡组检索1只恶魔族怪兽并覆盖(面朝下守备召唤)。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.summoner, AI_HINT.costHand]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        hand = self.searchCards(LOCATION.hand, self.getSide(), CARD_TYPE.all, self)
        if not hand:
            return False
        def isFiend(c):
            return c.race == RACE.FIEND
        targets = self.searchCards(LOCATION.deck, self.getSide(), CARD_TYPE.monster, self, isFiend)
        if not targets:
            return False
        if self.freeMonsterSpace() == 0:
            return False
        if justCheck:
            return True
        cost = yield self.y_select1Card(hand, TITLE.discard, canCancel=True)
        if not cost:
            return False
        chosen = yield self.y_select1Card(targets, TITLE.specialSummon, canCancel=True)
        if not chosen:
            return False
        yield self.y_sendCardToGrave(cost)
        self.saveTarget1(chosen)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1(checkLocationChange=False)
        if not t or self.freeMonsterSpace() == 0:
            return False
        # 覆盖:面朝下以守备表示放置
        yield self.y_specialSummon(t, form=FORM.defenceSet)
        return True
