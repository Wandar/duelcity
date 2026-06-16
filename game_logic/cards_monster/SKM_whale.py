# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Mechanical Whale
卡名:机器鲸鱼
效果:1T:<被破坏后>:自己抽1张卡。
"""

class SKM_whale(Card):
    CARD_KEY = 'SKM_whale'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(SKM_whale_e1)


class SKM_whale_e1(Effect):
    # 1T:<被破坏后>:自己抽1张卡。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.grave, [Signal.Destroyed])
    AI_HINT = [AI_HINT.drawCard]
    EFF_POWER = 2

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Destroyed, self.owner):
            return False
        if len(self.game.decks[self.getSide()]) < 1:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        yield self.y_drawCard(self.getSide(), 1)
        return True

