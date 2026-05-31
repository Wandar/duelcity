# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:hitfoot
卡名:hitfoot
"""
"""
1AI:当对方怪兽攻击时,使其受到200点伤害
"""
class thitfoot(Card):
    CARD_KEY="hitfoot"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(thitfoot_effect1)

class thitfoot_effect1(Effect):
    effType = EFF_TYPE.optionalInstant

    observeSignals = (LOCATION.spellTrapZone, [Signal.InBattle])

    AI_HINT = [AI_HINT.eraser]
    AI_POWER = 1

    def y_cost(self, justCheck:bool, signal:Signal.InBattle):
        if not (isSignal(signal, Signal.InBattle) and
                signal.attackerCard.side in self.getEnemySideTuple()):
            return False
        if justCheck:
            return True
        self.saveTarget1(signal.attackerCard)
        return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        attacker = self.getLegalTarget1()
        if attacker:
            yield self.y_addCardData(attacker, atkAdd=-200, defAdd=-200,
                                     effDuration=EFF_DURATION.utilBattleEnds)
        return True
