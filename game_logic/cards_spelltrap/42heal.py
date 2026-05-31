# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:42heal
卡名:42heal
"""

#########################my

"""
1A:选择自己场上一只{ATK}不满的怪兽,{ATK}+500
"""

class t42heal(Card):
    CARD_KEY="42heal"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(t42heal_effect1)

class t42heal_effect1(Effect):
    effType = EFF_TYPE.active

    observeSignals = (LOCATION.monsterZone,[Signal.NormalSummon])

    AI_HINT = [AI_HINT.addAtk]
    AI_POWER = 1

    def y_cost(self,justCheck:bool,signal):
        def f(card):
            return card.atk<card.atk_0
        myMonsters=self.searchCards(LOCATION.monsterZone,self.getSide(),filterFunc=f)

        if not len(myMonsters):
            return

        if justCheck:
            return True

        target=yield self.y_select1Card(myMonsters,TITLE.target,canCancel=True)
        if target:
            self.saveTarget1(target)
            return True

    def y_activate(self,justCheck:bool,signal):

        if justCheck:
            return True

        target=self.getLegalTarget1()
        if target:
            yield self.y_healCard(target,500)
