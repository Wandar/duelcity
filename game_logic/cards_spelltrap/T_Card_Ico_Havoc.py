# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_Havoc
卡名:混乱漩涡
"""

#########################my

"""
1A:破坏场上随机1张卡,然后自己从卡组抽1张
"""

class tT_Card_Ico_Havoc(Card):
    CARD_KEY="T_Card_Ico_Havoc"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_Havoc_effect1)

class tT_Card_Ico_Havoc_effect1(Effect):
    effType = EFF_TYPE.active


    AI_HINT = [AI_HINT.eraser]
    AI_POWER = 1

    def y_cost(self, justCheck:bool, signal):
        allField = self.searchCards(LOCATION.mask_onField, -1, CARD_TYPE.all, self)
        if self.owner in allField:
            allField.remove(self.owner)
        if not allField:
            return
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        import random
        allField = self.searchCards(LOCATION.mask_onField, -1, CARD_TYPE.all, self)
        if self.owner in allField:
            allField.remove(self.owner)
        if allField:
            victim = random.choice(allField)
            yield self.y_destroyCard(victim)
        if self.getDeckLeftNum():
            yield self.y_drawCard(self.getSide(), 1)
