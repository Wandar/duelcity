# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Druid8
卡名:藤蔓缠绕
"""

#########################my

"""
1I:对方怪兽攻击时,使其不能攻击直到下一回合结束
"""

class tT_Druid8(Card):
    CARD_KEY="T_Druid8"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Druid8_effect1)

class tT_Druid8_effect1(Effect):
    effType = EFF_TYPE.optionalInstant

    observeSignals = (LOCATION.spellTrapZone, [Signal.InBattle])

    AI_HINT = [AI_HINT.eraser]
    AI_POWER = 1

    def y_cost(self, justCheck:bool, signal):
        if not (isSignal(signal, Signal.InBattle) and signal.attackerCard.side in self.getEnemySideTuple()):
            return
        if justCheck:
            return True
        self.saveTarget1(signal.attackerCard)
        return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        yield self.y_cancelAttack(signal)
        target = self.getLegalTarget1()
        if target:
            yield self.y_silenceCard(target, EFF_DURATION.util2TurnEnds, self.uniID)
