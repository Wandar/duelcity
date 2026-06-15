# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_fission  【魔法】
卡图:深蓝背景,绿色旋转漩涡,五条黄色闪电末端各有小怪兽,裂变分裂。
效果(AOTIP):
1A:[解放自己场上1只怪兽]:裂变——从自己卡组特殊召唤最多3只星级低于被解放怪兽的怪兽。
"""

class tT_Card_Ico_fission(Card):
    CARD_KEY = "T_Card_Ico_fission"
    AUTHOR = "Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_fission_eff)

class tT_Card_Ico_fission_eff(Effect):
    effType = EFF_TYPE.active
    activateLocation = LOCATION.spellTrapZone
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 4
    fuelLevel = 0

    def y_cost(self, justCheck: bool, signal):
        myMons = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self)
        if not myMons: return False
        if justCheck: return True
        fuel = yield self.y_select1Card(myMons, TITLE.tribute, self.getSide(), canCancel=True)
        if not fuel: return False
        self.fuelLevel = fuel.level
        successNum = yield self.y_tributeCard(fuel)
        if not successNum: return False
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck: return True
        lv = self.fuelLevel
        cands = self.searchCards(LOCATION.deck, self.getSide(), CARD_TYPE.monster, self,
                                 lambda c: c.level < lv)
        if not cands: return False
        maxN = min(3, self.freeMonsterSpace(), len(cands))
        if maxN <= 0: return False
        chosen = yield self.y_selectCards(cands, TITLE.specialSummon, self.getSide(), 1, maxN, canCancel=True)
        if chosen:
            yield self.y_specialSummon(chosen, self.getSide())
        return True
