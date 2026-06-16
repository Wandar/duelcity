# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Batdrake
卡名:飞蝠龙
效果:1T:<战斗破坏对方怪兽时>:自己回复等同该怪兽原本攻击力的基本分。
"""

class Voidray(Card):
    CARD_KEY = 'Voidray'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Voidray_e1)


class Voidray_e1(Effect):
    # 1T:<战斗破坏对方怪兽时>:自己回复等同该怪兽原本攻击力的基本分。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.BattleFinish])
    AI_HINT = [AI_HINT.recoverLP]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.BattleFinish):
            return False
        if signal.attackerCard != self.owner:
            return False
        rc = signal.receiverCard
        if rc is None or rc.isMonsterOnField():
            return False
        if justCheck:
            return True
        self._heal = rc.atk_0
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        heal = getattr(self, "_heal", 0)
        if heal > 0:
            yield self.y_healPlayer(self.getSide(), heal)
        return True

