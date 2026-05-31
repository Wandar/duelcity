# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:handbook
卡名:handbook
"""
"""
1A:从卡组发现一张卡并覆盖
"""
class thandbook(Card):
    CARD_KEY="handbook"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(thandbook_effect1)

class thandbook_effect1(Effect):
    effType = EFF_TYPE.active

    AI_HINT = [AI_HINT.search]
    AI_POWER = 2

    def y_cost(self, justCheck:bool, signal):
        if not self.getDeckLeftNum():
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        card = yield self.y_discover1CardFromDeck()
        if card:
            yield self.y_setCardToSpellZone(card)
        return True
