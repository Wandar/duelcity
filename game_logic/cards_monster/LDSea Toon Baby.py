# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Sea Dragonling
卡名:海龙宝宝
效果:1T:<召唤时>:从卡组把1只「梦幻海龙」加入手牌。
"""

class LDSea_Toon_Baby(Card):
    CARD_KEY = 'LDSea Toon Baby'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(LDSea_Toon_Baby_e1)


class LDSea_Toon_Baby_e1(Effect):
    # 1T:<召唤时>:从卡组把1只「梦幻海龙」加入手牌。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.searchMonster]
    EFF_POWER = 2

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        def isT(c):
            return c.cardKey == "LDSea Toon"
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

