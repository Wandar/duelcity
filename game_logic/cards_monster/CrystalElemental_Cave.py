# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Crystal Elemental Guardian
卡名:水晶元素守护者
效果:1A:[丢弃1只岩石族怪兽]:发现一张等级5以下的岩石族怪兽并特殊召唤。2A:[支付800基本分]:对对方造成1200点伤害。
"""

class CrystalElemental_Cave(Card):
    CARD_KEY = "CrystalElemental_Cave"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(CrystalElemental_Cave_e1)
        self.initEffect(CrystalElemental_Cave_e2)


class CrystalElemental_Cave_e1(Effect):
    # 1A:[丢弃1只岩石族怪兽]:发现一张等级5以下的岩石族怪兽并特殊召唤。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.summoner, AI_HINT.costHand]
    EFF_POWER = 4

    def y_cost(self, justCheck, signal):
        def isRock(c):
            return c.race == RACE.ROCK
        fodder = self.searchCards(LOCATION.hand, self.getSide(), CARD_TYPE.monster, self, isRock)
        if not fodder:
            return False
        if self.freeMonsterSpace() == 0:
            return False
        if justCheck:
            return True
        cost = yield self.y_select1Card(fodder, TITLE.discard, canCancel=True)
        if not cost:
            return False
        yield self.y_sendCardToGrave(cost)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        if self.freeMonsterSpace() == 0:
            return False
        picked = yield self.y_discoverCard(title=TITLE.specialSummon, side=self.getSide(), race=RACE.ROCK,
                                           cardType=CARD_TYPE.monster, maxLevel=5, count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked)
        return True


class CrystalElemental_Cave_e2(Effect):
    # 2A:[支付800基本分]:对对方造成1200点伤害。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.damager, AI_HINT.highCost]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if self.game.LPs[self.getSide()] <= 800:
            return False
        if justCheck:
            return True
        yield self.y_damagePlayer(self.getSide(), 800)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        yield self.y_damagePlayer(self.getEnemySideTuple(), 1200)
        return True
