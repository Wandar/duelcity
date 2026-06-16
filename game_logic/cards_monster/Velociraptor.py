# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Velociraptor
卡名:迅猛龙
效果:1T:<召唤时>:从卡组检索一张「迅猛龙」。
"""

class Velociraptor(Card):
    CARD_KEY = 'Velociraptor'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Velociraptor_e1)


class Velociraptor_e1(Effect):
    # 1T:<召唤时>:从卡组检索一张「迅猛龙」。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.searchMonster]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        def isTarget(c):
            return c != self.owner and c.cardKey == "Velociraptor"
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

