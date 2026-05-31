# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_recycle
卡名:循环回收
"""

#########################my

"""
1A:[Cost:将自己手牌1张卡送去墓地]:把自己墓地1张魔法·陷阱卡加入手牌
"""

class tT_Card_Ico_recycle(Card):
    CARD_KEY="T_Card_Ico_recycle"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_recycle_effect1)

class tT_Card_Ico_recycle_effect1(Effect):
    effType = EFF_TYPE.active


    AI_HINT = [AI_HINT.earn]
    AI_POWER = 1

    def y_cost(self, justCheck:bool, signal):
        hand = self.game.hands[self.getSide()]
        if not hand:
            return
        grave = self.searchCards(LOCATION.graveyard, self.getSide(), CARD_TYPE.spell | CARD_TYPE.trap, self)
        if not grave:
            return
        if justCheck:
            return True
        discard = yield self.y_select1Card(hand, TITLE.sendToGrave, self.getSide(), canCancel=True)
        retrieve = yield self.y_select1Card(grave, TITLE.addToHand, canCancel=True)
        if discard and retrieve:
            yield self.y_sendCardToGrave(discard)
            self.saveTarget1(retrieve)
            return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        target = self.getLegalTarget1()
        if target:
            yield self.y_returnCardToHand(target, self.getSide())
