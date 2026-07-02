# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *



"""
1A:投掷一枚硬币,正面的情况抽一张卡,背面的情况从卡组覆盖一张卡
"""
class t50coin(Card):
    CARD_KEY="50coin"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(t50coin_effect1)

class t50coin_effect1(Effect):
    effType = EFF_TYPE.active


    AI_HINT = [AI_HINT.drawCard,AI_HINT.search]
    AI_POWER = 1
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True

        if randPercent(0.5):
            yield self.y_drawCard()
        else:
            yield self.y_setCardFromDeck(self.getSide(), 1)
        return True