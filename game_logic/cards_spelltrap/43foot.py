# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:43foot
卡名:43foot
"""

"""
1I:当对方怪兽攻击时,使其变为守备表示
"""

class t43foot(Card):
    CARD_KEY="43foot"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(t43foot_effect1)

class t43foot_effect1(Effect):
    effType = EFF_TYPE.optionalInstant

    observeSignals = (LOCATION.spellTrapZone,[Signal.InBattle])

    AI_HINT = [AI_HINT.eraser]
    AI_POWER = 1
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal:Signal.InBattle):
        if isSignal(signal,Signal.InBattle) and signal.attackerCard.side in self.getEnemySideTuple():
            pass
        else:
            return

        if justCheck:
            return True

        self.saveTarget1(signal.attackerCard)
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True

        target=self.getLegalTarget1()
        if target:
            yield self.y_changeForm(target, FORM.defence)
