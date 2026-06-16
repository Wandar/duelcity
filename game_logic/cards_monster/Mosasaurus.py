# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Mosasaurus
卡名:沧龙
效果:1I:<墓地效果:对方怪兽攻击宣言时>[除外此卡和墓地一只其他恐龙]:把该攻击怪兽返回持有者手牌。
"""

class Mosasaurus(Card):
    CARD_KEY = 'Mosasaurus'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Mosasaurus_e1)


class Mosasaurus_e1(Effect):
    # 1I:<墓地效果:对方怪兽攻击宣言时>[除外此卡和墓地一只其他恐龙]:把该攻击怪兽返回手牌。
    effType = EFF_TYPE.instant
    observeSignals = (LOCATION.grave, [Signal.RequestBattle])
    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.RequestBattle):
            return False
        if self.owner.location != LOCATION.grave:
            return False
        attacker = signal.attackerCard
        if attacker is None or self.checkAlly(attacker):
            return False
        def isOtherDino(c):
            return c != self.owner and c.race == RACE.DINOSAUR
        graveDinos = self.searchCards(LOCATION.grave, self.getSide(), CARD_TYPE.monster, self, isOtherDino)
        if not graveDinos:
            return False
        if justCheck:
            return True
        yield self.y_banishCard([self.owner, graveDinos[0]])
        self.saveTarget1(attacker)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1(checkLocationChange=False)
        if not t or not t.isMonsterOnField():
            return False
        yield self.y_returnCardToHand(t)
        return True

