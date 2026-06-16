# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Meadow Camo Chameleon Green
卡名:树影伪装者·绿
效果:1T:<被攻击时>:伤害计算前,此卡的守备力变为与攻击怪兽的攻击力相同{UTIL}。
"""

class ChameleonA(Card):
    CARD_KEY = 'ChameleonA'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(ChameleonA_e1)


class ChameleonA_e1(Effect):
    # 1T:<被攻击时>:伤害计算前,此卡的守备力变为与攻击怪兽的攻击力相同{UTIL}。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.RequestBattle])
    AI_HINT = [AI_HINT.battleBenefit]
    EFF_POWER = 2

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.RequestBattle):
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
        yield self.y_changeForm(self.owner, FORM.defence)
        yield self.y_changeCardData(self.owner, newDefence=attacker.atk, effDuration=EFF_DURATION.utilTurnEnds)
        return True

