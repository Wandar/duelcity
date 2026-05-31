# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_Made_In_Abyss
卡名:来自深渊
"""

#########################my

"""
1A:[Cost:支付1000基本分]:从卡组特殊召唤1只LV6以上的暗属性怪兽
"""

class tT_Card_Ico_Made_In_Abyss(Card):
    CARD_KEY="T_Card_Ico_Made_In_Abyss"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_Made_In_Abyss_effect1)

class tT_Card_Ico_Made_In_Abyss_effect1(Effect):
    effType = EFF_TYPE.active


    AI_HINT = [AI_HINT.summoner]
    AI_POWER = 1

    def y_cost(self, justCheck:bool, signal):
        if self.game.getPlayerLP(self.getSide()) <= 1000:
            return
        if not self.freeMonsterSpace():
            return
        if justCheck:
            return True
        yield self.y_damagePlayer(self.getSide(), 1000)
        return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        def f(c):
            return c.level >= 6 and c.attr == ATTR.DARK
        pool = self.searchCards(LOCATION.deck, self.getSide(), CARD_TYPE.monster, self, f)
        if pool:
            pick = yield self.y_select1Card(pool, TITLE.specialSummon, canCancel=True)
            if pick:
                yield self.y_specialSummon(pick, self.getSide(), FORM.attack)
