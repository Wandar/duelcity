# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_Demon_Form
卡名:恶魔形态
"""

#########################my

"""
1P:自己场上所有恶魔族怪兽的{ATK}+300。2T:<自己结束阶段>:自己从卡组抽1张
"""

class tT_Card_Ico_Demon_Form(Card):
    CARD_KEY="T_Card_Ico_Demon_Form"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_Demon_Form_effect1)

class tT_Card_Ico_Demon_Form_effect1(Effect):
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
            return c.race == RACE.FIEND
        mons = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self, f)
        for m in mons:
            yield self.y_addCardData(m, attackAdd=300, effDuration=EFF_DURATION.whileSourceExists, uniqueSourceID=self.uniID)
        # pseudo: on own end phase, draw 1
        yield self.y_registerEndPhaseTrigger(self.getSide(), action='draw1', sourceID=self.uniID)
