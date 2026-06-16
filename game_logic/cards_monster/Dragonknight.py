# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Crimsonscale Dragon Knight
卡名:赤鳞龙骑士
效果:1A:你控制龙族时,可从手牌特殊召唤此卡,之后从卡组把1张龙族加入手牌。
"""

class Dragonknight(Card):
    CARD_KEY = 'Dragonknight'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Dragonknight_e1)


class Dragonknight_e1(Effect):
    # 1A:你控制龙族时,可从手牌特殊召唤此卡,之后从卡组把1张龙族加入手牌。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.hand
    AI_HINT = [AI_HINT.summoner, AI_HINT.searchMonster]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if self.owner.location != LOCATION.hand:
            return False
        def isDragon(c):
            return c.race == RACE.DRAGON
        mine = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, None, isDragon)
        if not mine:
            return False
        if self.freeMonsterSpace() == 0:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        yield self.y_specialSummon(self.owner)
        def isDragon(c):
            return c.race == RACE.DRAGON
        targets = self.searchCards(LOCATION.deck, self.getSide(), CARD_TYPE.monster, self, isDragon)
        if targets:
            chosen = yield self.y_select1Card(targets, TITLE.addToHand, self.getSide(), canCancel=True)
            if chosen:
                yield self.y_returnCardToHand(chosen)
        return True

