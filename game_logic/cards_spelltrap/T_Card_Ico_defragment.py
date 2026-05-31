# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_defragment
卡名:碎片整理
"""

#########################my

"""
1A:将自己墓地中全部机械族怪兽洗回卡组,然后自己从卡组抽1张
"""

class tT_Card_Ico_defragment(Card):
    CARD_KEY="T_Card_Ico_defragment"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_defragment_effect1)

class tT_Card_Ico_defragment_effect1(Effect):
    effType = EFF_TYPE.active


    AI_HINT = [AI_HINT.drawCard]
    AI_POWER = 1

    def y_cost(self, justCheck:bool, signal):
        def f(c):
            return c.race == RACE.MACHINE
        pool = self.searchCards(LOCATION.graveyard, self.getSide(), CARD_TYPE.monster, self, f)
        if not pool:
            return
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        def f(c):
            return c.race == RACE.MACHINE
        pool = self.searchCards(LOCATION.graveyard, self.getSide(), CARD_TYPE.monster, self, f)
        for m in pool:
            yield self.y_returnCardToDeck(m, self.getSide(), RETURN_TO_DECK.shuffle)
        if self.getDeckLeftNum():
            yield self.y_drawCard(self.getSide(), 1)
