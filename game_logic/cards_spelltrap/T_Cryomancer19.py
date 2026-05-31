# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Cryomancer19
卡名:寒霜铠甲
"""

#########################my

"""
1P:自己场上水属性怪兽的{DEF}+500,并且不会被战斗破坏
"""

class tT_Cryomancer19(Card):
    CARD_KEY="T_Cryomancer19"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Cryomancer19_effect1)

class tT_Cryomancer19_effect1(Effect):
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
            return c.attr == ATTR.WATER
        mons = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self, f)
        for m in mons:
            yield self.y_addCardData(m, defenceAdd=500, effDuration=EFF_DURATION.whileSourceExists, uniqueSourceID=self.uniID)
            yield self.y_addImmunityBuffToCard(m, IMMUNITY_MASK.destroyByBattle,
                                                EFF_DURATION.whileSourceExists, self.uniID)
