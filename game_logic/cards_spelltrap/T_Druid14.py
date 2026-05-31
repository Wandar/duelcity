# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Druid14
卡名:自然庇护
"""

#########################my

"""
1P:自己场上植物族怪兽不会被战斗破坏
"""

class tT_Druid14(Card):
    CARD_KEY="T_Druid14"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Druid14_effect1)

class tT_Druid14_effect1(Effect):
    effType = EFF_TYPE.permanent


    AI_HINT = [AI_HINT.enhance]
    AI_POWER = 1

    def y_cost(self, justCheck:bool, signal):
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        def f(c):
            return c.race == RACE.PLANT
        mons = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self, f)
        for m in mons:
            yield self.y_addImmunityBuffToCard(m, IMMUNITY_MASK.destroyByBattle,
                                                EFF_DURATION.whileSourceExists, self.uniID)
