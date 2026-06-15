# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Rolling Hedgehog
卡名:滚滚刺猬
"""

class toon_Hedgehog(Card):
    CARD_KEY="toon_Hedgehog"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(toon_Hedgehog_e1)


"""
1A:[丢弃1张手牌]:对对方场上1只怪兽造成700点伤害。
"""
class toon_Hedgehog_e1(Effect):
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.damager]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        hand = self.searchCards(LOCATION.hand, self.getSide(), CARD_TYPE.all, self)
        if not hand:
            return False
        enemies = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self)
        if not enemies:
            return False
        if justCheck:
            return True
        discardCard = yield self.y_select1Card(hand, TITLE.discard, canCancel=True)
        if not discardCard:
            return False
        target = yield self.y_select1Card(enemies, TITLE.damage, canCancel=True)
        if not target:
            return False
        yield self.y_locationChange(discardCard, LOCATION.grave)
        self.saveTarget1(target)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        target = self.getLegalTarget1(checkLocationChange=False)
        if not target:
            return False
        yield self.y_damageCard(target, 700)
        return True
