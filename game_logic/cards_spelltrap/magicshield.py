# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:magicshield
卡名:magicshield
"""
"""
1I:当对方怪兽攻击时,使这次攻击无效
"""
class tmagicshield(Card):
    CARD_KEY="magicshield"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tmagicshield_effect1)

class tmagicshield_effect1(Effect):
    effType = EFF_TYPE.optionalInstant

    observeSignals = (LOCATION.spellTrapZone, [Signal.InBattle])

    AI_HINT = [AI_HINT.eraser]
    AI_POWER = 3

    def y_cost(self, justCheck:bool, signal:Signal.InBattle):
        if not (isSignal(signal, Signal.InBattle) and
                signal.attackerCard.side in self.getEnemySideTuple()):
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck:bool, signal:Signal.InBattle):
        if justCheck:
            return True
        yield self.y_cancelAttack(signal)
        return True
