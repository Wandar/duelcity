# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Cryomancer9
卡名:寒冰爆发
"""

#########################my

"""
1A:对方场上所有怪兽本回合不能攻击,并变为守备表示
"""

class tT_Cryomancer9(Card):
    CARD_KEY="T_Cryomancer9"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Cryomancer9_effect1)

class tT_Cryomancer9_effect1(Effect):
    effType = EFF_TYPE.active


    AI_HINT = [AI_HINT.eraser]
    AI_POWER = 1

    def y_cost(self, justCheck:bool, signal):
        eMon = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self)
        if not eMon:
            return
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        eMon = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self)
        for m in eMon:
            yield self.y_changeForm(m, FORM.defence)
            yield self.y_silenceCard(m, EFF_DURATION.utilTurnEnds, self.uniID)
