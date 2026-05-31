# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Cultist12
卡名:邪教恶物
"""

#########################my

"""
1A:[Cost:支付1000基本分]:从卡组特殊召唤1只LV4以下的暗属性怪兽
"""

class tT_Cultist12(Card):
    CARD_KEY="T_Cultist12"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Cultist12_effect1)

class tT_Cultist12_effect1(Effect):
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
            return c.level <= 4 and c.attr == ATTR.DARK
        pool = self.searchCards(LOCATION.deck, self.getSide(), CARD_TYPE.monster, self, f)
        if pool:
            pick = yield self.y_select1Card(pool, TITLE.specialSummon, canCancel=True)
            if pick:
                yield self.y_specialSummon(pick, self.getSide(), FORM.attack)
