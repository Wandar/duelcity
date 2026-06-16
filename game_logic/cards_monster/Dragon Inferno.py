# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Inferno Imp
卡名:爆炎小恶龙
效果:1T:此卡攻击的伤害计算前,可以破坏此卡,改为对攻击对象造成1000点伤害。
"""

class Dragon_Inferno(Card):
    CARD_KEY = 'Dragon Inferno'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Dragon_Inferno_e1)


class Dragon_Inferno_e1(Effect):
    # 1T:此卡攻击的伤害计算前,可以破坏此卡,改为对攻击对象造成1000点伤害。
    # NOTE: 取消原战斗的钩子未暴露,这里实现为破坏自身并对攻击对象造成1000伤害。
    effType = EFF_TYPE.optionalInstant
    observeSignals = (LOCATION.monsterZone, [Signal.InBattle])
    AI_HINT = [AI_HINT.damager]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.InBattle):
            return False
        if signal.attackerCard != self.owner:
            return False
        if not self.owner.isMonsterOnField():
            return False
        if justCheck:
            return True
        target = signal.receiverCard
        successNum = yield self.y_destroyCard(self.owner)
        if not successNum:
            return False
        self.saveTarget1(target)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1(checkLocationChange=False)
        if not t or not t.isMonsterOnField():
            return False
        yield self.y_damageCard(t, 1000)
        return True

