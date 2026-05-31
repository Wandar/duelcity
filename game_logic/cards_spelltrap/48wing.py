# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:48wing
卡名:48wing
"""

"""
1A:从手牌临时召唤一只LV4以下的怪兽
"""

class t48wing(Card):
    CARD_KEY="48wing"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(t48wing_effect1)

class t48wing_effect1(Effect):
    effType = EFF_TYPE.active

    AI_HINT = [AI_HINT.summoner]
    SCORE= 20

    def y_cost(self,justCheck:bool,signal):
        if not self.freeMonsterSpace():
            return
        handMonsters=self.searchCards(LOCATION.hand,self.getSide(),CARD_TYPE.monster,self,lambda card:card.canSpecialSummon() and card.level<4)
        if not handMonsters:
            return

        if justCheck:
            return True

        target=yield self.y_select1Card(handMonsters,TITLE.specialSummon,canCancel=True)
        if target:
            self.saveTarget1(target)
            return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True

        target=self.getLegalTarget1()
        yield self.y_specialSummon(target)
