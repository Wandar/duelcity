# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Pastureland Dragon
卡名:牧野之龙
效果:1T:<对方召唤怪兽时>:对该怪兽造成800点伤害。
"""

class plainsdragon(Card):
    CARD_KEY = 'plainsdragon'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(plainsdragon_e1)


class plainsdragon_e1(Effect):
    # 1T:<对方召唤怪兽时>:对该怪兽造成800点伤害。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.damager]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon):
            return False
        scard = getattr(signal, "card", None)
        if scard is None or scard == self.owner or self.checkAlly(scard):
            return False
        if not scard.isMonsterOnField():
            return False
        if not self.owner.isMonsterOnField():
            return False
        if justCheck:
            return True
        self.saveTarget1(scard)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1()
        if not t:
            return False
        yield self.y_damageCard(t, 800)
        return True

