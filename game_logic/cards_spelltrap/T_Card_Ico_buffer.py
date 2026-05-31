# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_buffer
卡名:缓冲护盾
"""

#########################my

"""
1I:对方怪兽攻击时,将其战斗伤害减半
"""

class tT_Card_Ico_buffer(Card):
    CARD_KEY="T_Card_Ico_buffer"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_buffer_effect1)

class tT_Card_Ico_buffer_effect1(Effect):
    effType = EFF_TYPE.optionalInstant

    observeSignals = (LOCATION.spellTrapZone, [Signal.InBattle])

    AI_HINT = [AI_HINT.enhance]
    AI_POWER = 1

    def y_cost(self, justCheck:bool, signal):
        if not (isSignal(signal, Signal.InBattle) and signal.attackerCard.side in self.getEnemySideTuple()):
            return
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        # pseudo: halve upcoming battle damage for this attack
        yield self.y_modifyBattleDamage(signal, multiplier=0.5)
