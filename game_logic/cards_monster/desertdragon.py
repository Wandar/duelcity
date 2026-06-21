# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Flaming Sand Dragon
卡名:烈焰沙龙
效果:1A:[丢弃1张手牌]:破坏对方场上1只怪兽。
"""

class desertdragon(Card):
    CARD_KEY = "desertdragon"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(desertdragon_e1)


class desertdragon_e1(Effect):
    # 1A:[丢弃1张手牌]:破坏对方场上1只怪兽。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 4

    def y_cost(self, justCheck, signal):
        hand = self.searchCards(LOCATION.hand, self.getSide(), CARD_TYPE.all, self)
        if not hand:
            return False
        enemies = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self)
        if not enemies:
            return False
        if justCheck:
            return True
        discard = yield self.y_select1Card(hand, TITLE.discard, canCancel=True)
        if not discard:
            return False
        t = yield self.y_select1Card(enemies, TITLE.destroy, canCancel=True)
        if not t:
            return False
        yield self.y_locationChange(discard, LOCATION.grave)
        self.saveTarget1(t)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1()
        if not t:
            return False
        yield self.y_destroyCard(t)
        return True
