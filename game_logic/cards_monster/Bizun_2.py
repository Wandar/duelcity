# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Bramble Rampage Tusker
卡名:棘丛暴獠
效果:1T:<被破坏后>:发现1张「棘丛」怪兽卡并特殊召唤。
"""

class Bizun_2(Card):
    CARD_KEY = "Bizun_2"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Bizun_2_e1)


class Bizun_2_e1(Effect):
    # 1T:<被破坏后>:发现1张「棘丛」怪兽卡并特殊召唤。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.grave, [Signal.Destroyed])
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Destroyed, self.owner):
            return False
        if self.freeMonsterSpace() == 0:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        def isBizun(c):
            return "Bizun" in c.cardKey
        picked = yield self.y_discoverCard(side=self.getSide(), cardType=CARD_TYPE.monster,
                                           filterFunc=isBizun, count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked)
        return True
