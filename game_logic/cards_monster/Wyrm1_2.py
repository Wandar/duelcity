# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Emerald Crystal Lizard
卡名:碧空晶蜥
效果:1A:[把1只其他怪兽解放]:发现一张等级5以下的龙族怪兽并特殊召唤。2A:[丢弃1张手牌]:从卡组检索1只龙族怪兽并覆盖。
"""

class Wyrm1_2(Card):
    CARD_KEY = 'Wyrm1_2'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Wyrm1_2_e1)
        self.initEffect(Wyrm1_2_e2)


class Wyrm1_2_e1(Effect):
    # 1A:[把1只其他怪兽解放]:发现一张等级5以下的龙族怪兽并特殊召唤。
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
        picked = yield self.y_discoverCard(side=self.getSide(), race=RACE.DRAGON,
                                           cardType=CARD_TYPE.monster, maxLevel=5, count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked)
        return True


class Wyrm1_2_e2(Effect):
    # 2A:[丢弃1张手牌]:从卡组检索1只龙族怪兽并覆盖。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.summoner, AI_HINT.costHand]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        hand = self.searchCards(LOCATION.hand, self.getSide(), CARD_TYPE.all, self)
        if not hand:
            return False
        def isR(c):
            return c.race == RACE.DRAGON
        targets = self.searchCards(LOCATION.deck, self.getSide(), CARD_TYPE.monster, self, isR)
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
        yield self.y_specialSummon(t, form=FORM.defenceSet)
        return True
