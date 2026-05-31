# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_master_of_tactics
卡名:战术大师
"""

#########################my

"""
1A:本回合自己场上所有怪兽可以直接攻击,但{ATK}-400
"""

class tT_Card_Ico_master_of_tactics(Card):
    CARD_KEY="T_Card_Ico_master_of_tactics"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_master_of_tactics_effect1)

class tT_Card_Ico_master_of_tactics_effect1(Effect):
    effType = EFF_TYPE.active


    AI_HINT = [AI_HINT.addAtk]
    AI_POWER = 1

    def y_cost(self, justCheck:bool, signal):
        myMon = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self)
        if not myMon:
            return
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        myMon = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self)
        for m in myMon:
            yield self.y_addCardData(m, attackAdd=-400, effDuration=EFF_DURATION.utilTurnEnds)
            # pseudo: grant direct-attack permission for this turn
            yield self.y_grantDirectAttack(m, EFF_DURATION.utilTurnEnds, self.uniID)
