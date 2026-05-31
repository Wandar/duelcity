# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:49flyshoe
卡名:49flyshoe
"""

"""
1A:[Cost:一只本回合攻击过的怪兽返回手牌]:从手牌额外召唤一只LV6以下的怪兽
"""

class t49flyshoe(Card):
    CARD_KEY="49flyshoe"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(t49flyshoe_effect1)

class t49flyshoe_effect1(Effect):
    effType = EFF_TYPE.active


    AI_HINT = [AI_HINT.eraser]
    AI_POWER = 1
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        if not self.freeExtraSummonChance():
            return

        monsters=self.searchCards(LOCATION.monsterZone,self.getSide(),CARD_TYPE.monster,None,lambda card:card.attackCntThisTurn!=0 and card.canExtraSummon())

        if not monsters:
            return

        handLV6=self.searchCards(LOCATION.hand,self.getSide(),CARD_TYPE.monster,self,lambda card:card.level<=6)
        if not handLV6:
            return

        if justCheck:
            return True

        tribute=yield self.y_select1Card(monsters,TITLE.returnToHand,canCancel=True)
        target=yield self.y_select1Card(handLV6,TITLE.specialSummon,canCancel=True)
        if tribute and target:
            yield self.y_sendCardToGrave(tribute)
            self.saveTarget1(target)
            return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True

        target=self.getLegalTarget1()
        if target:
            yield self.y_extraSummon(target)
