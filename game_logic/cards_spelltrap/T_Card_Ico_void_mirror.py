# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_void_mirror
卡名:虚空镜像
"""

#########################my

"""
1I:对方怪兽效果将自己作为对象时,使那次效果反弹给对方
"""

class tT_Card_Ico_void_mirror(Card):
    CARD_KEY="T_Card_Ico_void_mirror"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_void_mirror_effect1)

class tT_Card_Ico_void_mirror_effect1(Effect):
    effType = EFF_TYPE.optionalInstant

    observeSignals = (LOCATION.spellTrapZone, [Signal.BeforeActivateEffect])

    AI_HINT = [AI_HINT.eraser]
    AI_POWER = 1

    def y_cost(self, justCheck:bool, signal):
        if not isSignal(signal, Signal.BeforeActivateEffect):
            return
        srcCard = getattr(signal, 'sourceCard', None)
        if not srcCard or srcCard.side not in self.getEnemySideTuple():
            return
        if not (srcCard.cardType & CARD_TYPE.monster):
            return
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        # pseudo: retarget the opposing monster effect back at its controller
        yield self.y_redirectEffectToSource(signal)
