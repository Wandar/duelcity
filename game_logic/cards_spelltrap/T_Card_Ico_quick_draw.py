# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_quick_draw
卡名:疾速抽牌
"""

#########################my

"""
1A:自己从卡组抽2张,然后从手牌把1张卡送去墓地
"""

class tT_Card_Ico_quick_draw(Card):
    CARD_KEY="T_Card_Ico_quick_draw"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_quick_draw_effect1)

class tT_Card_Ico_quick_draw_effect1(Effect):
    effType = EFF_TYPE.active


    AI_HINT = [AI_HINT.drawCard]
    AI_POWER = 1

    def y_cost(self, justCheck:bool, signal):
        if self.getDeckLeftNum() < 1:
            return
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        yield self.y_drawCard(self.getSide(), 2)
        hand = self.game.hands[self.getSide()]
        if hand:
            pick = yield self.y_select1Card(hand, TITLE.sendToGrave, self.getSide(), canCancel=False)
            if pick:
                yield self.y_sendCardToGrave(pick)
