# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_necronomicurse
卡名:死灵诅咒
"""

#########################my

"""
1P:这张卡不能从场上离开,除非被其他卡效果破坏
"""

class tT_Card_Ico_necronomicurse(Card):
    CARD_KEY="T_Card_Ico_necronomicurse"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_necronomicurse_effect1)

class tT_Card_Ico_necronomicurse_effect1(Effect):
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
        # pseudo: make self untargetable by normal return-to-hand/deck effects
        yield self.y_addImmunityBuffToCard(self.owner, IMMUNITY_MASK.returnToHand | IMMUNITY_MASK.returnToDeck,
                                            EFF_DURATION.whileSourceExists, self.uniID)
