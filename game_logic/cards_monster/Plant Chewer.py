# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Pumpkin Orb
卡名:南瓜球
效果:1A:[把自己场上1只其他植物族怪兽送入弃牌区]:自己抽2张卡。
"""

class Plant_Chewer(Card):
    CARD_KEY = 'Plant Chewer'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Plant_Chewer_e1)


class Plant_Chewer_e1(Effect):
    # 1A:[把自己场上1只其他植物族怪兽送入弃牌区]:自己抽2张卡。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.drawCard, AI_HINT.costMonster]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        def isFodder(c):
            return c != self.owner and c.race == RACE.PLANT
        fodder = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self, isFodder)
        if not fodder:
            return False
        if len(self.game.decks[self.getSide()]) < 1:
            return False
        if justCheck:
            return True
        cost = yield self.y_select1Card(fodder, TITLE.sendToGrave, canCancel=True)
        if not cost:
            return False
        yield self.y_sendCardToGrave(cost)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        n = min(2, len(self.game.decks[self.getSide()]))
        if n > 0:
            yield self.y_drawCard(self.getSide(), n)
        return True

