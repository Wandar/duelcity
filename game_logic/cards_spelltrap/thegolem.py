# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:thegolem
卡名:魔像降临
"""

#########################my

"""
1A:从卡组特殊召唤1只LV4以下的岩石族怪兽,以守备表示
"""

class tthegolem(Card):
    CARD_KEY="thegolem"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tthegolem_effect1)

class tthegolem_effect1(Effect):
    effType = EFF_TYPE.active


    AI_HINT = [AI_HINT.summoner]
    AI_POWER = 1

    def y_cost(self, justCheck:bool, signal):
        def f(c):
            return c.level <= 4 and c.race == RACE.ROCK
        pool = self.searchCards(LOCATION.deck, self.getSide(), CARD_TYPE.monster, self, f)
        if not pool:
            return
        if not self.freeMonsterSpace():
            return
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        def f(c):
            return c.level <= 4 and c.race == RACE.ROCK
        pool = self.searchCards(LOCATION.deck, self.getSide(), CARD_TYPE.monster, self, f)
        if pool:
            pick = yield self.y_select1Card(pool, TITLE.specialSummon, canCancel=True)
            if pick:
                yield self.y_specialSummon(pick, self.getSide(), FORM.defence)
