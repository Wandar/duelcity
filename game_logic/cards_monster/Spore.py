# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Spore Orb
卡名:孢子球
效果:1T:<被破坏后>:从卡组把2只「孢子球」以守备表示特殊召唤。
"""

class Spore(Card):
    CARD_KEY = 'Spore'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Spore_e1)


class Spore_e1(Effect):
    # 1T:<被破坏后>:从卡组把2只「孢子球」以守备表示特殊召唤。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.grave, [Signal.Destroyed])
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Destroyed, self.owner):
            return False
        def isSpore(c):
            return c.cardKey == "Spore"
        targets = self.searchCards(LOCATION.deck, self.getSide(), CARD_TYPE.monster, self, isSpore)
        if not targets:
            return False
        if self.freeMonsterSpace() == 0:
            return False
        if justCheck:
            return True
        self.saveTarget1(targets[:2])
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        targets = self.getLegalTarget1(checkLocationChange=False)
        if not targets:
            return False
        if type(targets) != list:
            targets = [targets]
        yield self.y_specialSummon(targets, form=FORM.defence)
        return True

