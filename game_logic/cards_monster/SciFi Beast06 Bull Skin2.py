# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Mechabeast Bull
卡名:百兽机 牛怪
效果:1A:[把此卡解放]:从手牌·卡组把1只"百兽机"怪兽特殊召唤。
"""

class SciFi_Beast06_Bull_Skin2(Card):
    CARD_KEY = 'SciFi Beast06 Bull Skin2'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(SciFi_Beast06_Bull_Skin2_e1)


class SciFi_Beast06_Bull_Skin2_e1(Effect):
    # 1A:[把此卡解放]:从手牌·卡组把1只"百兽机"怪兽特殊召唤。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 3
    FAMILY = ("SciFi Beast03 Skin1", "SciFi Beast04 WhaleSnake Skin1", "SciFi Beast05_Skin1",
              "SciFi Beast06 Bull Skin2", "Sci-Fi Dragon Skin4")

    def y_cost(self, justCheck, signal):
        def isFamily(c):
            return c != self.owner and c.cardKey in self.FAMILY
        targets = self.searchCards(LOCATION.hand | LOCATION.deck, self.getSide(), CARD_TYPE.monster, self, isFamily)
        if not targets:
            return False
        if justCheck:
            return True
        chosen = yield self.y_select1Card(targets, TITLE.specialSummon, canCancel=True)
        if not chosen:
            return False
        successNum = yield self.y_tributeCard(self.owner)
        if not successNum:
            return False
        self.saveTarget1(chosen)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1(checkLocationChange=False)
        if not t or self.freeMonsterSpace() == 0:
            return False
        yield self.y_specialSummon(t)
        return True

