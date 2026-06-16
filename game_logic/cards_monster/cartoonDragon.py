# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Tiny Purple Dragon
卡名:小紫龙
效果:1T:<召唤时>:双方各从自己卡组顶端把2张卡送入弃牌区。
"""

class cartoonDragon(Card):
    CARD_KEY = 'cartoonDragon'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(cartoonDragon_e1)


class cartoonDragon_e1(Effect):
    # 1T:<召唤时>:双方各从自己卡组顶端把2张卡送入弃牌区。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.botDontUse]
    EFF_POWER = 2

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        for side in (self.getSide(),) + tuple(self.getEnemySideTuple()):
            deck = self.game.decks[side]
            top = deck[-2:]
            if top:
                yield self.y_sendCardToGrave(list(top))
        return True

