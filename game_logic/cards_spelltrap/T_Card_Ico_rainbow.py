# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_rainbow
卡名:彩虹多样
"""

#########################my

"""
1A:从卡组随机发现3只不同属性的怪兽,选1只特殊召唤
"""

class tT_Card_Ico_rainbow(Card):
    CARD_KEY="T_Card_Ico_rainbow"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_rainbow_effect1)

class tT_Card_Ico_rainbow_effect1(Effect):
    effType = EFF_TYPE.active


    AI_HINT = [AI_HINT.summoner]
    AI_POWER = 1

    def y_cost(self, justCheck:bool, signal):
        if not self.getDeckLeftNum():
            return
        if not self.freeMonsterSpace():
            return
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        # pseudo: discover 3 monsters with distinct attrs from deck
        picks = yield self.y_discoverNMonstersFromDeckDistinctAttr(3)
        if picks:
            chosen = yield self.y_select1Card(picks, TITLE.specialSummon, canCancel=True)
            if chosen:
                yield self.y_specialSummon(chosen, self.getSide(), FORM.attack)
