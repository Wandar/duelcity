# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Giant Mouth Thorn King
卡名:巨嘴刺王
效果:1P:此卡被攻击的伤害计算后,攻击怪兽的控制者受到400点伤害。
"""

class Cactus_Boss(Card):
    CARD_KEY = 'Cactus Boss'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Cactus_Boss_e1)


class Cactus_Boss_e1(Effect):
    # 1P:此卡被攻击的伤害计算后,攻击怪兽的控制者受到400点伤害。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.BattleFinish])
    AI_HINT = [AI_HINT.damager]
    EFF_POWER = 2

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.BattleFinish):
            return False
        if signal.receiverCard != self.owner:
            return False
        if signal.attackerCard is None:
            return False
        if justCheck:
            return True
        self.saveTarget1(signal.attackerCard)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        attacker = self.getLegalTarget1(checkLocationChange=False)
        if not attacker:
            return False
        yield self.y_damagePlayer(attacker.side, 400)
        return True

