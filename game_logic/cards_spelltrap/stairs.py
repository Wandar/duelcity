# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:stairs
卡名:stairs
"""
"""
1A:[Cost:1000LP]:从卡组随机覆盖两只怪兽
"""
class tstairs(Card):
    CARD_KEY="stairs"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tstairs_effect1)

class tstairs_effect1(Effect):
    effType = EFF_TYPE.active

    AI_HINT = [AI_HINT.search]
    AI_POWER = 2

    def y_cost(self, justCheck:bool, signal):
        if self.game.getPlayerLP(self.getSide()) <= 1000:
            return False
        if not self.getDeckLeftNum():
            return False
        if justCheck:
            return True
        yield self.y_dealDamage(self.getSide(), 1000)
        return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        yield self.y_setCardFromDeck(self.getSide(), 2, randomPick=True, cardType=CARD_TYPE.monster)
        return True
