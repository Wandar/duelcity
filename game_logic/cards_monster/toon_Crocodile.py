# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Fiercy Crocodile
卡名:凶凶鳄鱼
"""

class toon_Crocodile(Card):
    CARD_KEY="toon_Crocodile"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(toon_Crocodile_e1)


"""
1I:<墓地效果:对方怪兽直接攻击宣言时>[除外此卡]:对该攻击怪兽造成1000点伤害。
"""
class toon_Crocodile_e1(Effect):
    effType = EFF_TYPE.instant
    observeSignals = (LOCATION.grave, [Signal.RequestBattle])
    AI_HINT = [AI_HINT.damager]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal: Signal.RequestBattle):
        if not isSignal(signal, Signal.RequestBattle):
            return False
        if signal.battleType != BATTLE_TYPE.directAttack:
            return False
        if self.owner.location != LOCATION.grave:
            return False
        attacker = signal.attackerCard
        if attacker is None or attacker.side == self.getSide():
            return False
        if justCheck:
            return True
        successNum = yield self.y_banishCard(self.owner)
        if not successNum:
            return False
        self.saveTarget1(attacker)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        target = self.getLegalTarget1(checkLocationChange=False)
        if not target:
            return False
        yield self.y_damageCard(target, 1000)
        return True
