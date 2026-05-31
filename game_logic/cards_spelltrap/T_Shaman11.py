# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Shaman11
卡名:萨满战士
"""

#########################my

"""
1A:[Cost:从手牌丢弃1只LV4以下怪兽]:自己从卡组抽1张,然后{ATK}+300
"""

class tT_Shaman11(Card):
    CARD_KEY="T_Shaman11"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Shaman11_effect1)

class tT_Shaman11_effect1(Effect):
    effType = EFF_TYPE.active


    AI_HINT = [AI_HINT.drawCard]
    AI_POWER = 1

    def y_cost(self, justCheck:bool, signal):
        def f(c):
            return (c.cardType & CARD_TYPE.monster) and c.level <= 4
        hand = [c for c in self.game.hands[self.getSide()] if f(c)]
        if not hand:
            return
        if not self.getDeckLeftNum():
            return
        myMon = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self)
        if not myMon:
            return
        if justCheck:
            return True
        discard = yield self.y_select1Card(hand, TITLE.sendToGrave, self.getSide(), canCancel=True)
        target = yield self.y_select1Card(myMon, TITLE.target, canCancel=True)
        if discard and target:
            yield self.y_sendCardToGrave(discard)
            self.saveTarget1(target)
            return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        yield self.y_drawCard(self.getSide(), 1)
        target = self.getLegalTarget1()
        if target:
            yield self.y_addCardData(target, attackAdd=300, effDuration=EFF_DURATION.utilTurnEnds)
