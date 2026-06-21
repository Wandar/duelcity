# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Stegosaurus
卡名:剑龙
效果:1T:守备表示的此卡被攻击的伤害计算后,破坏攻击怪兽。
"""

class Stegosaurus(Card):
    CARD_KEY = "Stegosaurus"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Stegosaurus_e1)


class Stegosaurus_e1(Effect):
    # 1T:守备表示的此卡被攻击的伤害计算后,破坏攻击怪兽。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.BattleFinish])
    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.BattleFinish):
            return False
        if signal.receiverCard != self.owner:
            return False
        if self.owner.form not in (FORM.defence, FORM.defenceSet):
            return False
        attacker = signal.attackerCard
        if attacker is None or not attacker.isMonsterOnField():
            return False
        if justCheck:
            return True
        self.saveTarget1(attacker)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1()
        if not t:
            return False
        yield self.y_destroyCard(t)
        return True
