# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_reinforced_body
卡名:强化身体
"""

#########################my

"""
1A:选择自己场上1只怪兽,使其{DEF}+1000直到回合结束
"""

class tT_Card_Ico_reinforced_body(Card):
    CARD_KEY="T_Card_Ico_reinforced_body"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_reinforced_body_effect1)

class tT_Card_Ico_reinforced_body_effect1(Effect):
    effType = EFF_TYPE.active


    AI_HINT = [AI_HINT.enhance]
    AI_POWER = 1

    def y_cost(self, justCheck:bool, signal):
        myMon = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self)
        if not myMon:
            return
        if justCheck:
            return True
        target = yield self.y_select1Card(myMon, TITLE.target, canCancel=True)
        if target:
            self.saveTarget1(target)
            return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        target = self.getLegalTarget1()
        if target:
            yield self.y_addCardData(target, defenceAdd=1000, effDuration=EFF_DURATION.utilTurnEnds)
