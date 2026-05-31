# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Arcanist4
卡名:T_Arcanist4
"""
"""
1A:当对方怪兽攻击时,结束此次战斗阶段
"""
class tT_Arcanist4(Card):
    CARD_KEY="T_Arcanist4"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Arcanist4_effect1)

class tT_Arcanist4_effect1(Effect):
    effType = EFF_TYPE.optionalInstant

    observeSignals = (LOCATION.spellTrapZone, [Signal.InBattle])

    AI_HINT = [AI_HINT.eraser]
    AI_POWER = 3

    def y_cost(self, justCheck:bool, signal:Signal.InBattle):
        if isSignal(signal, Signal.InBattle) and signal.attackerCard.side in self.getEnemySideTuple():
            pass
        else:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        yield self.game.y_changePhase(PHASE.mainphase2)
        return True
