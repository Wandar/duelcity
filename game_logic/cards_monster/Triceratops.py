# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Triceratops
卡名:三角龙
效果:1T:<手牌效果:自己的恐龙族怪兽被攻击时>:把此卡特殊召唤。
"""

class Triceratops(Card):
    CARD_KEY = 'Triceratops'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Triceratops_e1)


class Triceratops_e1(Effect):
    # 1T:<手牌效果:自己的恐龙族怪兽被攻击时>:把此卡特殊召唤。
    effType = EFF_TYPE.instant
    observeSignals = (LOCATION.hand, [Signal.RequestBattle])
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 2

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.RequestBattle):
            return False
        if self.owner.location != LOCATION.hand:
            return False
        rc = signal.receiverCard
        if rc is None or not self.checkAlly(rc) or rc.race != RACE.DINOSAUR:
            return False
        if self.freeMonsterSpace() == 0:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        yield self.y_specialSummon(self.owner)
        return True

