# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_Metallicize
卡名:金属化
"""

#########################my

"""
1P:自己受到的所有战斗伤害减少300
"""

class tT_Card_Ico_Metallicize(Card):
    CARD_KEY="T_Card_Ico_Metallicize"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_Metallicize_effect1)

class tT_Card_Ico_Metallicize_effect1(Effect):
    effType = EFF_TYPE.permanent


    AI_HINT = [AI_HINT.enhance]
    AI_POWER = 1

    def y_cost(self, justCheck:bool, signal):
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        # pseudo: persistent -300 to all battle damage received
        yield self.y_addPlayerBuff(self.getSide(), PLAYER_BUFF.reduceBattleDamage300,
                                    EFF_DURATION.whileSourceExists, self.uniID)
