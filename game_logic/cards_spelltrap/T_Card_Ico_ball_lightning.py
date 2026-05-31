# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_ball_lightning
卡名:球形闪电
"""

#########################my

"""
1A:选择场上1只怪兽,使其{ATK}-600直到回合结束
"""

class tT_Card_Ico_ball_lightning(Card):
    CARD_KEY="T_Card_Ico_ball_lightning"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_ball_lightning_effect1)

class tT_Card_Ico_ball_lightning_effect1(Effect):
    effType = EFF_TYPE.active


    AI_HINT = [AI_HINT.debuff]
    AI_POWER = 1

    def y_cost(self, justCheck:bool, signal):
        mons = self.searchCards(LOCATION.monsterZone, -1, CARD_TYPE.monster, self)
        if not mons:
            return
        if justCheck:
            return True
        target = yield self.y_select1Card(mons, TITLE.target, canCancel=True)
        if target:
            self.saveTarget1(target)
            return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        target = self.getLegalTarget1()
        if target:
            yield self.y_addCardData(target, attackAdd=-600, effDuration=EFF_DURATION.utilTurnEnds)
