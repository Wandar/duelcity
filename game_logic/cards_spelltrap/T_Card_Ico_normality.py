# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_normality
卡名:常态化
"""

#########################my

"""
1P:只要这张卡存在,场上所有怪兽的效果都无效化
"""

class tT_Card_Ico_normality(Card):
    CARD_KEY="T_Card_Ico_normality"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_normality_effect1)

class tT_Card_Ico_normality_effect1(Effect):
    effType = EFF_TYPE.permanent


    AI_HINT = [AI_HINT.eraser]
    AI_POWER = 1

    def y_cost(self, justCheck:bool, signal):
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        allMon = self.searchCards(LOCATION.monsterZone, -1, CARD_TYPE.monster, self)
        for m in allMon:
            yield self.y_silenceCard(m, EFF_DURATION.whileSourceExists, self.uniID)
