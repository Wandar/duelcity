# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:429sword
卡名:429sword
"""
"""
1A:[Cost:献祭一只怪兽]:选择一只怪兽增加{ATK}200,从卡组随机覆盖一张卡
"""
class t429sword(Card):
    CARD_KEY="429sword"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(t429sword_effect1)

class t429sword_effect1(Effect):
    effType = EFF_TYPE.active

    AI_HINT = [AI_HINT.addAtk, AI_HINT.search]
    AI_POWER = 2

    def y_cost(self, justCheck:bool, signal):
        myMonsters = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self)
        if not myMonsters:
            return False
        if justCheck:
            return True
        tribute = yield self.y_select1Card(myMonsters, TITLE.tribute, canCancel=True)
        if not tribute:
            return False
        yield self.y_tributeCard([tribute])
        allMonsters = self.searchCards(LOCATION.monsterZone, -1, CARD_TYPE.monster, self)
        if not allMonsters:
            return True
        buffTarget = yield self.y_select1Card(allMonsters, TITLE.target, canCancel=True)
        if buffTarget:
            self.saveTarget1(buffTarget)
        return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        target = self.getLegalTarget1()
        if target:
            yield self.y_addCardData(target, attackAdd=200, effDuration=EFF_DURATION.onceForever)
        yield self.y_setCardFromDeck(self.getSide(), 1, randomPick=True)
        return True
