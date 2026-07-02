# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:diggem
卡名:diggem
"""
"""
1A:从卡组顶部覆盖一张卡
"""
class tdiggem(Card):
    CARD_KEY="diggem"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tdiggem_effect1)

class tdiggem_effect1(Effect):
    effType = EFF_TYPE.active

    AI_HINT = [AI_HINT.search]
    AI_POWER = 1

    def y_cost(self, justCheck:bool, signal):
        if not self.getDeckLeftNum():
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        yield self.y_setCardFromDeck(self.getSide(), 1)
        return True
