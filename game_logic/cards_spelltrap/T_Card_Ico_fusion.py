# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_fusion
卡名:融合涌动
"""

#########################my

"""
1A:[Cost:从手牌·场上送出2只指定怪兽]:从额外卡组特殊召唤1只融合怪兽
"""

class tT_Card_Ico_fusion(Card):
    CARD_KEY="T_Card_Ico_fusion"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_fusion_effect1)

class tT_Card_Ico_fusion_effect1(Effect):
    effType = EFF_TYPE.active


    AI_HINT = [AI_HINT.summoner]
    AI_POWER = 1

    def y_cost(self, justCheck:bool, signal):
        handMon = [c for c in self.game.hands[self.getSide()] if c.cardType & CARD_TYPE.monster]
        fieldMon = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self)
        pool = handMon + fieldMon
        if len(pool) < 2:
            return
        extraPool = self.searchCards(LOCATION.extraDeck, self.getSide(), CARD_TYPE.fusion, self)
        if not extraPool:
            return
        if not self.freeMonsterSpace():
            return
        if justCheck:
            return True
        materials = yield self.y_selectCards(pool, TITLE.fusionMaterial, self.getSide(), 2, 2, canCancel=True)
        if materials and len(materials) == 2:
            self.saveTarget1(materials)
            return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        materials = self.getLegalTarget1() or []
        for m in materials:
            yield self.y_sendCardToGrave(m)
        extraPool = self.searchCards(LOCATION.extraDeck, self.getSide(), CARD_TYPE.fusion, self)
        if extraPool:
            pick = yield self.y_select1Card(extraPool, TITLE.specialSummon, canCancel=True)
            if pick:
                yield self.y_specialSummon(pick, self.getSide(), FORM.attack)
