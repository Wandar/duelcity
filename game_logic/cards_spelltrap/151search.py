# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:151search
卡名:151search
"""

"""
1A:从卡组随机发现一只怪兽,然后覆盖
"""

class t151search(Card):
    CARD_KEY="151search"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(t151search_effect1)

class t151search_effect1(Effect):
    effType = EFF_TYPE.active


    AI_HINT = [AI_HINT.searchMonster]
    AI_POWER = 1


    def y_activate(self,justCheck:bool,signal):
        if not self.getDeckLeftNum():
            return

        if justCheck:
            return True

        card=yield self.y_discover1MonsterFromDeck()
        if card:
            yield self.y_setCardToSpellZone(card)
        return True
