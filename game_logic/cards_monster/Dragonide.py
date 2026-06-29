# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Hammer Lizard
卡名:铁锤蜥蜴
effect:
效果:1T:<战斗破坏对方怪兽时>:对对方造成500点伤害。
"""

class Dragonide(Card):
    CARD_KEY = "Dragonide"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Dragonide_e1)


class Dragonide_e1(Effect):
    # 1T:<战斗破坏对方怪兽时>:对对方造成500点伤害。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.BattleFinish])
    AI_HINT = [AI_HINT.damager]
    EFF_POWER = 2

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
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        yield self.y_damagePlayer(self.getEnemySideTuple(), 500)
        return True
