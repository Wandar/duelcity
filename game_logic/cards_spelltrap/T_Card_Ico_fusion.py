# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_fusion  【魔法】
卡图:紫黑背景,戴帽角色左臂冰晶右臂闪电,中央橙色太阳光环,融合力量。
效果(AOTIP):
1A:[解放自己场上2只怪兽]:融合——发现1只星级等于两者星级合计(上限12)的怪兽,把它特殊召唤。
"""

class tT_Card_Ico_fusion(Card):
    CARD_KEY = "T_Card_Ico_fusion"
    AUTHOR = "Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_fusion_eff)

class tT_Card_Ico_fusion_eff(Effect):
    effType = EFF_TYPE.active
    activateLocation = LOCATION.spellTrapZone
    AI_HINT = [AI_HINT.summoner, AI_HINT.costMonster]
    EFF_POWER = 4
    fuseLevel = 0

    def y_cost(self, justCheck: bool, signal):
        myMons = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self)
        if len(myMons) < 2: return False
        if justCheck: return True
        chosen = yield self.y_selectCards(myMons, TITLE.tribute, self.getSide(), 2, 2, canCancel=True)
        if not chosen or len(chosen) < 2: return False
        self.fuseLevel = min(12, max(1, sum(c.level for c in chosen)))
        successNum = yield self.y_tributeCard(chosen)
        if not successNum: return False
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck: return True
        lv = self.fuseLevel
        self.fuseLevel = 0
        if lv <= 0 or not self.freeMonsterSpace(): return False
        picked = yield self.y_discoverCard(title=TITLE.specialSummon, side=self.getSide(), cardType=CARD_TYPE.monster,
                                           minLevel=lv, maxLevel=lv, count=3, canCancel=True)
        if picked and self.freeMonsterSpace():
            yield self.y_specialSummon(picked, self.getSide())
        return True
