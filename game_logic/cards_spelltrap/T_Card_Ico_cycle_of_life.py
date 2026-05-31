# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_cycle_of_life
卡名:生命循环
"""

#########################my

"""
1A:[Cost:将自己墓地1只植物族怪兽除外]:从卡组抽1张,然后回复500基本分
"""

class tT_Card_Ico_cycle_of_life(Card):
    CARD_KEY="T_Card_Ico_cycle_of_life"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_cycle_of_life_effect1)

class tT_Card_Ico_cycle_of_life_effect1(Effect):
    effType = EFF_TYPE.active


    AI_HINT = [AI_HINT.drawCard]
    AI_POWER = 1

    def y_cost(self, justCheck:bool, signal):
        def f(c):
            return c.race == RACE.PLANT
        plants = self.searchCards(LOCATION.graveyard, self.getSide(), CARD_TYPE.monster, self, f)
        if not plants:
            return
        if not self.getDeckLeftNum():
            return
        if justCheck:
            return True
        pick = yield self.y_select1Card(plants, TITLE.banish, canCancel=True)
        if pick:
            yield self.y_banishCard(pick)
            return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        yield self.y_drawCard(self.getSide(), 1)
        yield self.y_healPlayer(self.getSide(), 500)
