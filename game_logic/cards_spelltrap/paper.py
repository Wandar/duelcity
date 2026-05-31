# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:paper
卡名:paper
"""
"""
1A:从卡组发现一只怪兽覆盖,然后让自己场上一只怪兽{ATK}+200
"""
class tpaper(Card):
    CARD_KEY="paper"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tpaper_effect1)

class tpaper_effect1(Effect):
    effType = EFF_TYPE.active

    AI_HINT = [AI_HINT.search, AI_HINT.addAtk]
    AI_POWER = 2

    def y_cost(self, justCheck:bool, signal):
        if not self.getDeckLeftNum():
            return False
        myMonsters = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self)
        if not myMonsters:
            return False
        if justCheck:
            return True
        target = yield self.y_select1Card(myMonsters, TITLE.target, canCancel=True)
        if target:
            self.saveTarget1(target)
            return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        card = yield self.y_discover1MonsterFromDeck()
        if card:
            yield self.y_setCardToSpellZone(card)
        target = self.getLegalTarget1()
        if target:
            yield self.y_addCardData(target, atkAdd=200, effDuration=EFF_DURATION.utilTurnEnds)
        return True
