# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Cloudhoof
卡名:云云麟角
效果:1T:<召唤时>:把对方场上1只怪兽返回持有者手牌,然后自己抽1张卡。
"""

class cartoonKirin(Card):
    CARD_KEY = 'cartoonKirin'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(cartoonKirin_e1)


class cartoonKirin_e1(Effect):
    # 1T:<召唤时>:把对方场上1只怪兽返回持有者手牌,然后自己抽1张卡。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.eraser, AI_HINT.drawCard]
    EFF_POWER = 4

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        enemies = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self)
        if not enemies:
            return False
        if justCheck:
            return True
        t = yield self.y_select1Card(enemies, TITLE.returnToHand, canCancel=True)
        if not t:
            return False
        self.saveTarget1(t)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1()
        if not t:
            return False
        yield self.y_returnCardToHand(t)
        if len(self.game.decks[self.getSide()]) > 0:
            yield self.y_drawCard(self.getSide(), 1)
        return True
