# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Cultist17
卡名:邪教仪式
"""

#########################my

"""
1A:[Cost:解放自己场上1只怪兽]:从卡组特殊召唤1只比其等级高1级的暗属性怪兽
"""

class tT_Cultist17(Card):
    CARD_KEY="T_Cultist17"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Cultist17_effect1)

class tT_Cultist17_effect1(Effect):
    effType = EFF_TYPE.active


    AI_HINT = [AI_HINT.summoner]
    AI_POWER = 1

    def y_cost(self, justCheck:bool, signal):
        myMon = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self)
        if not myMon:
            return
        if justCheck:
            return True
        target = yield self.y_select1Card(myMon, TITLE.tribute, canCancel=True)
        if target:
            self.saveTarget1(target)
            return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        sac = self.getLegalTarget1()
        if not sac:
            return
        targetLv = sac.level + 1
        yield self.y_tributeCard(sac)
        def f(c):
            return c.level == targetLv and c.attr == ATTR.DARK
        pool = self.searchCards(LOCATION.deck, self.getSide(), CARD_TYPE.monster, self, f)
        if pool:
            pick = yield self.y_select1Card(pool, TITLE.specialSummon, canCancel=True)
            if pick:
                yield self.y_specialSummon(pick, self.getSide(), FORM.attack)
