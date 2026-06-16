# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Rat Assassin
卡名:鼠刺客
效果:1T:<召唤时>:从卡组把1只「鼠兵」加入手牌。
"""

class RatAssassinDefault(Card):
    CARD_KEY = 'RatAssassinDefault'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(RatAssassinDefault_e1)


class RatAssassinDefault_e1(Effect):
    # 1T:<召唤时>:从卡组把1只「鼠兵」加入手牌。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.searchMonster]
    EFF_POWER = 2

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        def isT(c):
            return c != self.owner and c.cardKey == "RatAssassinDefault"
        targets = self.searchCards(LOCATION.deck, self.getSide(), CARD_TYPE.monster, self, isT)
        if not targets:
            return False
        if justCheck:
            return True
        self.saveTarget1(targets[0])
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1()
        if not t:
            return False
        yield self.y_returnCardToHand(t)
        return True

