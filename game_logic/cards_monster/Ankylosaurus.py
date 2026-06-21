# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Ankylosaurus
卡名:甲龙
效果:1T:<召唤时>:发现1张恐龙族怪兽卡。
"""

class Ankylosaurus(Card):
    CARD_KEY = "Ankylosaurus"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Ankylosaurus_e1)


class Ankylosaurus_e1(Effect):
    # 1T:<召唤时>:发现1张恐龙族怪兽卡。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.searchMonster]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        yield self.y_discoverCard(side=self.getSide(), race=RACE.DINOSAUR,
                                  cardType=CARD_TYPE.monster, count=3, canCancel=True)
        return True
