# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Cryomancer5
卡名:冰霜箭
"""

#########################my

"""
1A:选择对方场上1只怪兽,使其{ATK}-500并不能攻击
"""

class tT_Cryomancer5(Card):
    CARD_KEY="T_Cryomancer5"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Cryomancer5_effect1)

class tT_Cryomancer5_effect1(Effect):
    effType = EFF_TYPE.active


    AI_HINT = [AI_HINT.debuff]
    AI_POWER = 1

    def y_cost(self, justCheck:bool, signal):
        eMon = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self)
        if not eMon:
            return
        if justCheck:
            return True
        target = yield self.y_select1Card(eMon, TITLE.target, canCancel=True)
        if target:
            self.saveTarget1(target)
            return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        target = self.getLegalTarget1()
        if target:
            yield self.y_addCardData(target, attackAdd=-500, effDuration=EFF_DURATION.utilTurnEnds)
            yield self.y_silenceCard(target, EFF_DURATION.utilTurnEnds, self.uniID)
