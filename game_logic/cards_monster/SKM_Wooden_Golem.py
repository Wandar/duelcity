# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Wildwood Golem
卡名:荒野木傀儡
效果:1T:<召唤时>:查看卡组顶2张,1张加入手牌,1张放回。
"""

class SKM_Wooden_Golem(Card):
    CARD_KEY = 'SKM_Wooden_Golem'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(SKM_Wooden_Golem_e1)


class SKM_Wooden_Golem_e1(Effect):
    # 1T:<召唤时>:查看卡组顶2张,1张加入手牌,1张放回。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.earn]
    EFF_POWER = 2

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        if len(self.game.decks[self.getSide()]) < 1:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        deck = self.game.decks[self.getSide()]
        top = list(reversed(deck[-2:]))
        if not top:
            return False
        chosen = yield self.y_select1Card(top, TITLE.addToHand, self.getSide(), canCancel=True)
        if chosen:
            yield self.y_returnCardToHand(chosen)
        return True

