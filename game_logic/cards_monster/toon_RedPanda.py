# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Roundy Red Panda
卡名:团团小熊猫
"""

class toon_RedPanda(Card):
    CARD_KEY="toon_RedPanda"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(toon_RedPanda_e1)


"""
1T:<手牌效果:自己召唤兽族怪兽时>:把此卡特殊召唤。
"""
class toon_RedPanda_e1(Effect):
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.hand, [Signal.Summon])
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon):
            return False
        if self.owner.location != LOCATION.hand:
            return False
        c = signal.card
        if c is None or c == self.owner:
            return False
        if c.side != self.getSide():
            return False
        if c.race != RACE.BEAST:
            return False
        if self.freeMonsterSpace() == 0:
            return False
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        yield self.y_specialSummon(self.owner)
        return True
