# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Tiny Red Dragon
卡名:小红龙
效果:1A:[支付800基本分]:发现一张等级2以下的龙族怪兽并守备召唤。
"""

class cartoonWyvern(Card):
    CARD_KEY = "cartoonWyvern"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(cartoonWyvern_e1)


class cartoonWyvern_e1(Effect):
    # 1A:[支付800基本分]:发现一张等级2以下的龙族怪兽并守备召唤。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.summoner, AI_HINT.highCost]
    EFF_POWER = 3

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
        picked = yield self.y_discoverCard(title=TITLE.specialSummon, side=self.getSide(), race=RACE.DRAGON,
                                           cardType=CARD_TYPE.monster, maxLevel=2, count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked, form=FORM.defence)
        return True
