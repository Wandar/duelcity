# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_dark_harvest
卡名:黑暗收割
"""

#########################my

"""
1A:[Cost:解放自己场上1只怪兽]:从卡组抽2张
"""

class tT_Card_Ico_dark_harvest(Card):
    CARD_KEY="T_Card_Ico_dark_harvest"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_dark_harvest_effect1)

class tT_Card_Ico_dark_harvest_effect1(Effect):
    effType = EFF_TYPE.active


    AI_HINT = [AI_HINT.drawCard]
    AI_POWER = 1

    def y_cost(self, justCheck:bool, signal):
        myMon = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self)
        if not myMon:
            return
        if self.getDeckLeftNum() < 1:
            return
        if justCheck:
            return True
        target = yield self.y_select1Card(myMon, TITLE.tribute, canCancel=True)
        if target:
            yield self.y_tributeCard(target)
            return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        yield self.y_drawCard(self.getSide(), 2)
