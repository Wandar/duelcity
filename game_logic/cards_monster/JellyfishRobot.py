# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Jellyfish Robot
卡名:水母机器人
效果:1I:<被攻击时>:攻击怪兽受到400点伤害。
"""

class JellyfishRobot(Card):
    CARD_KEY = 'JellyfishRobot'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(JellyfishRobot_e1)


class JellyfishRobot_e1(Effect):
    # 1I:<被攻击时>:攻击怪兽受到400点伤害。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.RequestBattle])
    AI_HINT = [AI_HINT.damager]
    EFF_POWER = 2

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.RequestBattle):
            return False
        if signal.receiverCard != self.owner:
            return False
        attacker = signal.attackerCard
        if attacker is None:
            return False
        if justCheck:
            return True
        self.saveTarget1(attacker)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1(checkLocationChange=False)
        if not t or not t.isMonsterOnField():
            return False
        yield self.y_damageCard(t, 400)
        return True

