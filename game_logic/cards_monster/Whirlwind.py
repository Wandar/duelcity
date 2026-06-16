# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Tiny Breeze Sprite
卡名:微风小精灵
效果:1T:<召唤时>:从卡组把1只等级1的风属性怪兽加入手牌。
"""

class Whirlwind(Card):
    CARD_KEY = 'Whirlwind'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Whirlwind_e1)


class Whirlwind_e1(Effect):
    # 1T:<召唤时>:从卡组把1只等级1的风属性怪兽加入手牌。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.searchMonster]
    EFF_POWER = 2

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        def isT(c):
            return c.attr == ATTR.WIND and c.level == 1
        targets = self.searchCards(LOCATION.deck, self.getSide(), CARD_TYPE.monster, self, isT)
        if not targets:
            return False
        if justCheck:
            return True
        chosen = yield self.y_select1Card(targets, TITLE.addToHand, canCancel=True)
        if not chosen:
            return False
        self.saveTarget1(chosen)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1()
        if not t:
            return False
        yield self.y_returnCardToHand(t)
        return True

