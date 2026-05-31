# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_marionette
卡名:傀儡操纵
"""

#########################my

"""
1A:选择对方场上1只LV4以下的怪兽,直到回合结束获得其控制权
"""

class tT_Card_Ico_marionette(Card):
    CARD_KEY="T_Card_Ico_marionette"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_marionette_effect1)

class tT_Card_Ico_marionette_effect1(Effect):
    effType = EFF_TYPE.active


    AI_HINT = [AI_HINT.eraser]
    AI_POWER = 1

    def y_cost(self, justCheck:bool, signal):
        def f(c):
            return c.level <= 4
        eMon = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self, f)
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
            yield self.y_changeMonsterController(target, self.getSide(), EFF_DURATION.utilTurnEnds, self.uniID)
