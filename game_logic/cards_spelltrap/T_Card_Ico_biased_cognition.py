# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_biased_cognition
卡名:偏倚认知
"""

#########################my

"""
1P:自己场上所有怪兽的{ATK}+500。2T:<自己结束阶段>:自己从手牌丢弃1张
"""

class tT_Card_Ico_biased_cognition(Card):
    CARD_KEY="T_Card_Ico_biased_cognition"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_biased_cognition_effect1)

class tT_Card_Ico_biased_cognition_effect1(Effect):
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
        myMon = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self)
        for m in myMon:
            yield self.y_addCardData(m, attackAdd=500, effDuration=EFF_DURATION.whileSourceExists, uniqueSourceID=self.uniID)
        # pseudo: on own end phase, discard 1 hand
        yield self.y_registerEndPhaseTrigger(self.getSide(), action='discard1Hand', sourceID=self.uniID)
