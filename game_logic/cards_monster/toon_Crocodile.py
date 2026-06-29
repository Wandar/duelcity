# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Fiercy Crocodile
卡名:凶凶鳄鱼
效果:1A:[支付800基本分]:发现一张等级4以下的兽族怪兽并特殊召唤。2A:[丢弃1张手牌]:从卡组检索1只兽族怪兽并覆盖。
"""

class toon_Crocodile(Card):
    CARD_KEY = "toon_Crocodile"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(toon_Crocodile_e1)
        self.initEffect(toon_Crocodile_e2)


class toon_Crocodile_e1(Effect):
    # 1A:[支付800基本分]:发现一张等级4以下的兽族怪兽并特殊召唤。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.summoner, AI_HINT.highCost]
    EFF_POWER = 4

    def y_cost(self, justCheck, signal):
        if self.game.LPs[self.getSide()] <= 800:
            return False
        if self.freeMonsterSpace() == 0:
            return False
        if justCheck:
            return True
        yield self.y_damagePlayer(self.getSide(), 800)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        if self.freeMonsterSpace() == 0:
            return False
        picked = yield self.y_discoverCard(side=self.getSide(), race=RACE.BEAST,
                                           cardType=CARD_TYPE.monster, maxLevel=4, count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked)
        return True


class toon_Crocodile_e2(Effect):
    # 2A:[丢弃1张手牌]:从卡组检索1只兽族怪兽并覆盖(面朝下守备召唤)。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.summoner, AI_HINT.costHand]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        hand = self.searchCards(LOCATION.hand, self.getSide(), CARD_TYPE.all, self)
        if not hand:
            return False
        def isBeast(c):
            return c.race == RACE.BEAST
        targets = self.searchCards(LOCATION.deck, self.getSide(), CARD_TYPE.monster, self, isBeast)
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
