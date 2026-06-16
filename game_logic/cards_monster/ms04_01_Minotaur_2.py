# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Little Minotaur Warrior
卡名:牛头小战士
效果:1T:<被战斗破坏后>:从卡组把1只「米诺陶」加入手牌。
"""

class ms04_01_Minotaur_2(Card):
    CARD_KEY = 'ms04_01_Minotaur_2'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(ms04_01_Minotaur_2_e1)


class ms04_01_Minotaur_2_e1(Effect):
    # 1T:<被战斗破坏后>:从卡组把1只「米诺陶」加入手牌。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.grave, [Signal.DestroyedByBattle])
    AI_HINT = [AI_HINT.searchMonster]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.DestroyedByBattle, self.owner):
            return False
        def isTarget(c):
            return c.cardKey == "minotaur"
        targets = self.searchCards(LOCATION.deck, self.getSide(), CARD_TYPE.monster, self, isTarget)
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

