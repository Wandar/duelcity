# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Dragonknight14
卡名:龙晶
"""

#########################my

"""
1P:自己场上龙族怪兽的{ATK}+400
"""

class tT_Dragonknight14(Card):
    CARD_KEY="T_Dragonknight14"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Dragonknight14_effect1)

class tT_Dragonknight14_effect1(Effect):
    effType = EFF_TYPE.permanent


    AI_HINT = [AI_HINT.addAtk]
    AI_POWER = 1

    def y_cost(self, justCheck:bool, signal):
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        def f(c):
            return c.race == RACE.DRAGON
        mons = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self, f)
        for m in mons:
            yield self.y_addCardData(m, attackAdd=400, effDuration=EFF_DURATION.whileSourceExists, uniqueSourceID=self.uniID)
