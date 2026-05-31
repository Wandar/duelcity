# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_Disarm
卡名:缴械
"""

#########################my

"""
1I:对方怪兽攻击时,使其本回合不能攻击,并{ATK}-500
"""

class tT_Card_Ico_Disarm(Card):
    CARD_KEY="T_Card_Ico_Disarm"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_Disarm_effect1)

class tT_Card_Ico_Disarm_effect1(Effect):
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
        target = self.getLegalTarget1()
        if target:
            yield self.y_cancelAttack(signal)
            yield self.y_addCardData(target, attackAdd=-500, effDuration=EFF_DURATION.utilTurnEnds)
            yield self.y_silenceCard(target, EFF_DURATION.utilTurnEnds, self.uniID)
