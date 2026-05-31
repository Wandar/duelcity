# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_Obsidian_Skin
卡名:黑曜之肤
"""

#########################my

"""
1P:自己场上所有怪兽的{DEF}+500,并且不会被效果破坏
"""

class tT_Card_Ico_Obsidian_Skin(Card):
    CARD_KEY="T_Card_Ico_Obsidian_Skin"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_Obsidian_Skin_effect1)

class tT_Card_Ico_Obsidian_Skin_effect1(Effect):
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
        myMon = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self)
        for m in myMon:
            yield self.y_addCardData(m, defenceAdd=500, effDuration=EFF_DURATION.whileSourceExists, uniqueSourceID=self.uniID)
            yield self.y_addImmunityBuffToCard(m, IMMUNITY_MASK.destroyByEffect,
                                                EFF_DURATION.whileSourceExists, self.uniID)
