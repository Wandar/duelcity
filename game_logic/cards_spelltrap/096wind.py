# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:096wind
卡名:096wind
"""

"""
1A:从墓地守备表示临时召唤一只LV4以下的怪兽
"""

class t096wind(Card):
    CARD_KEY="096wind"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(t096wind_effect1)

class t096wind_effect1(Effect):
    effType = EFF_TYPE.active

    AI_HINT = [AI_HINT.eraser]
    AI_POWER = 1
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        if not self.freeMonsterSpace():
            return

        if justCheck:
            num=1
        else:
            num=9999
        graveMonsters=self.searchCards(LOCATION.grave,0,CARD_TYPE.monster,self,lambda card:card.canSpecialSummon(),num)
        if not graveMonsters:
            return
        if justCheck:
            return True

        target=yield self.y_select1Card(graveMonsters,TITLE.specialSummon)
        if target:
            self.saveTarget1(target)
            return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True

        target=self.getLegalTarget1()
        if target:#TODO
            yield self.y_specialSummon(target)
        return True
