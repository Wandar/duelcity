# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_eclipse
卡名:日食
"""

#########################my

"""
1A:本回合双方不能发动魔法·陷阱效果,直到结束阶段
"""

class tT_Card_Ico_eclipse(Card):
    CARD_KEY="T_Card_Ico_eclipse"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_eclipse_effect1)

class tT_Card_Ico_eclipse_effect1(Effect):
    effType = EFF_TYPE.active


    AI_HINT = [AI_HINT.eraser]
    AI_POWER = 1

    enemy = 0
    def y_cost(self, justCheck:bool, signal):
        if justCheck:
            return True
        self.enemy = yield self.y_select1EnemySide()
        return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        # pseudo: lock both players from activating spell/trap effects this turn
        for side in (self.getSide(), self.enemy):
            yield self.y_addPlayerBuff(side, PLAYER_BUFF.silenceSpellTrap, EFF_DURATION.utilTurnEnds, self.uniID)
