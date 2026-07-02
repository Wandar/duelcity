# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_Evolve  【魔法】
卡图:蓝绿背景,三个由小到大排列的绿色生物剪影,展现进化演变。
效果(AOTIP):
1A:[解放自己场上1只怪兽]:发现1只星级等于被解放怪兽星级+3(上限12)的怪兽,把它特殊召唤(进化)。
"""

class tT_Card_Ico_Evolve(Card):
    CARD_KEY = "T_Card_Ico_Evolve"
    AUTHOR = "Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_Evolve_eff)

class tT_Card_Ico_Evolve_eff(Effect):
    effType = EFF_TYPE.active
    activateLocation = LOCATION.spellTrapZone
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 4
    targetLevel = 0

    def y_cost(self, justCheck: bool, signal):
        myMons = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self)
        if not myMons: return False
        if justCheck: return True
        t = yield self.y_select1Card(myMons, TITLE.tribute, self.getSide(), canCancel=True)
        if not t: return False
        self.targetLevel = min(12, t.level + 3)
        successNum = yield self.y_tributeCard(t)
        if not successNum: return False
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck: return True
        lv = self.targetLevel
        self.targetLevel = 0
        if lv <= 0 or not self.freeMonsterSpace(): return False
        picked = yield self.y_discoverCard(title=TITLE.specialSummon, side=self.getSide(), cardType=CARD_TYPE.monster,
                                           minLevel=lv, maxLevel=lv, count=3, canCancel=True)
        if picked and self.freeMonsterSpace():
            yield self.y_specialSummon(picked, self.getSide())
        return True
