# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Lava Scarlet Dragon
卡名:熔岩绯龙
效果:1T:<战斗破坏对方怪兽时>:对对方造成被破坏怪兽原本攻击力一半的伤害。
"""

class Dragon_Rd(Card):
    CARD_KEY = 'Dragon_Rd'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Dragon_Rd_e1)


class Dragon_Rd_e1(Effect):
    # 1T:<战斗破坏对方怪兽时>:对对方造成被破坏怪兽原本攻击力一半的伤害。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.BattleFinish])
    AI_HINT = [AI_HINT.damager]
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
        self._dmg = rc.atk_0 // 2
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        dmg = getattr(self, "_dmg", 0)
        if dmg > 0:
            yield self.y_damagePlayer(self.getEnemySideTuple(), dmg)
        return True

