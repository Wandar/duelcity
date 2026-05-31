# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_undo
卡名:撤销
"""

#########################my

"""
1I:对方发动的效果处理后,使那次发动无效,该卡返回手牌
"""

class tT_Card_Ico_undo(Card):
    CARD_KEY="T_Card_Ico_undo"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_undo_effect1)

class tT_Card_Ico_undo_effect1(Effect):
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
        if justCheck:
            return True
        self.saveTarget1(srcCard)
        return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        yield self.y_counterEffectActivate(signal)
        yield self.y_returnCardToHand(self.owner, self.getSide())
