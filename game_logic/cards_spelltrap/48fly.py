# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:48fly
卡名:48fly
"""

"""
1A:[Cost:从手牌丢弃一只LV2以下的怪兽]:抽一张牌,从卡组覆盖一张卡
"""

class t48fly(Card):
    CARD_KEY="48fly"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(t48fly_effect1)

class t48fly_effect1(Effect):
    effType = EFF_TYPE.active

    observeSignals = (LOCATION.monsterZone,[Signal.NormalSummon])

    AI_HINT = [AI_HINT.drawCard]
    AI_POWER = 1
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        handMonsters=self.searchCards(LOCATION.hand,self.getSide(),CARD_TYPE.monster,filterFunc=lambda card:card.level<=2)

        if not handMonsters:
            return
        if justCheck:
            return True

        target=yield self.y_select1Card(handMonsters,TITLE.sendToGrave,canCancel=True)
        if target:
            yield self.saveTarget1(target)
            return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True

        yield self.y_drawCard(self.getSide())
        yield self.y_setCardFromDeck(self.getSide(), 1)
        return True
