# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_shadow_call
卡名:影子召唤
"""

#########################my

"""
1A:从自己墓地特殊召唤1只LV4以下的暗属性怪兽,以守备表示
"""

class tT_Card_Ico_shadow_call(Card):
    CARD_KEY="T_Card_Ico_shadow_call"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_shadow_call_effect1)

class tT_Card_Ico_shadow_call_effect1(Effect):
    effType = EFF_TYPE.active


    AI_HINT = [AI_HINT.summoner]
    AI_POWER = 1

    def y_cost(self, justCheck:bool, signal):
        def f(c):
            return c.level <= 4 and c.attr == ATTR.DARK
        pool = self.searchCards(LOCATION.graveyard, self.getSide(), CARD_TYPE.monster, self, f)
        if not pool:
            return
        if not self.freeMonsterSpace():
            return
        if justCheck:
            return True
        target = yield self.y_select1Card(pool, TITLE.specialSummon, canCancel=True)
        if target:
            self.saveTarget1(target)
            return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        target = self.getLegalTarget1()
        if target:
            yield self.y_specialSummon(target, self.getSide(), FORM.defence)
