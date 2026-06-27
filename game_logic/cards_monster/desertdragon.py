# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Flaming Sand Dragon
卡名:烈焰沙龙
effect:
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
    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        myHands = self.game.hands[self.getSide()]
        if not myHands:
            return False
        enemies = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(),
                                   CARD_TYPE.monster, self)
        if not enemies:
            return False
        if justCheck:
            return True

        discard = yield self.y_select1Card(myHands, TITLE.sendToGrave, canCancel=True)
        if not discard:
            return False
        target = yield self.y_select1Card(enemies, TITLE.destroy, canCancel=True)
        if not target:
            return False
        yield self.y_sendCardToGrave(discard)
        self.saveTarget1(target)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        target = self.getLegalTarget1()
        if not target:
            return False
        yield self.y_destroyCard(target)
        return True
