# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_Bioforge
卡名:生体锻造
"""

#########################my

"""
1A:从卡组随机发现一只生物族怪兽,特殊召唤到自己场上
"""

class tT_Card_Ico_Bioforge(Card):
    CARD_KEY="T_Card_Ico_Bioforge"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_Bioforge_effect1)

class tT_Card_Ico_Bioforge_effect1(Effect):
    effType = EFF_TYPE.active


    AI_HINT = [AI_HINT.searchMonster]
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
        card = yield self.y_discover1MonsterFromDeck()
        if card:
            yield self.y_specialSummon(card, self.getSide(), FORM.attack)
