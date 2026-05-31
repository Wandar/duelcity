# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:bonethunder
卡名:bonethunder
"""
"""
1A:选择自己场上一只LV4以下的怪兽,从卡组·墓地特殊召唤最多两张同名卡
"""
class tbonethunder(Card):
    CARD_KEY="bonethunder"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tbonethunder_effect1)

class tbonethunder_effect1(Effect):
    effType = EFF_TYPE.active

    AI_HINT = [AI_HINT.summoner]
    AI_POWER = 3

    def y_cost(self, justCheck:bool, signal):
        myLV4 = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self,
                                  lambda c: c.level <= 4)
        if not myLV4:
            return False
        if justCheck:
            return True
        target = yield self.y_select1Card(myLV4, TITLE.target, canCancel=True)
        if target:
            self.saveTarget1(target)
            return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        base = self.getLegalTarget1()
        if not base:
            return False
        sameNameCards = self.searchCards(LOCATION.deck, self.getSide(), CARD_TYPE.monster, self,
                                          lambda c: c.cardKey == base.cardKey)
        sameNameCards += self.searchCards(LOCATION.grave, self.getSide(), CARD_TYPE.monster, self,
                                           lambda c: c.cardKey == base.cardKey
                                                     and c.canSpecialSummon())
        import random
        random.shuffle(sameNameCards)
        for card in sameNameCards[:2]:
            yield self.y_specialSummon(card)
        return True
