# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:thedark
卡名:暗之领主
"""

#########################my

"""
1A:[Cost:支付1500基本分]:从卡组特殊召唤1只LV6以上的暗属性怪兽
"""

class tthedark(Card):
    CARD_KEY="thedark"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tthedark_effect1)

class tthedark_effect1(Effect):
    effType = EFF_TYPE.active


    AI_HINT = [AI_HINT.summoner]
    AI_POWER = 1

    def y_cost(self, justCheck:bool, signal):
        if self.game.getPlayerLP(self.getSide()) <= 1500:
            return
        if not self.freeMonsterSpace():
            return
        if justCheck:
            return True
        yield self.y_damagePlayer(self.getSide(), 1500)
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
