# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Cold Blue Werewolf
卡名:寒蓝恶狼
效果:1I:<手牌效果:对方怪兽攻击宣言时>[丢弃此卡]:该攻击怪兽变为守备表示。
"""

class Werewolf(Card):
    CARD_KEY = 'Werewolf'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Werewolf_e1)


class Werewolf_e1(Effect):
    # 1I:<手牌效果:对方怪兽攻击宣言时>[丢弃此卡]:该攻击怪兽变为守备表示。
    effType = EFF_TYPE.instant
    observeSignals = (LOCATION.hand, [Signal.RequestBattle])
    AI_HINT = [AI_HINT.debuff]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.RequestBattle):
            return False
        if self.owner.location != LOCATION.hand:
            return False
        attacker = signal.attackerCard
        if attacker is None or self.checkAlly(attacker):
            return False
        if justCheck:
            return True
        yield self.y_sendCardToGrave(self.owner)
        self.saveTarget1(attacker)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1(checkLocationChange=False)
        if not t or not t.isMonsterOnField():
            return False
        yield self.y_changeForm(t, FORM.defence)
        return True

