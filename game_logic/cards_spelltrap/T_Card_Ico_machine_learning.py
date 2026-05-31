# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_machine_learning
卡名:机器学习
"""

#########################my

"""
1T:<自己准备阶段>:自己从卡组抽1张
"""

class tT_Card_Ico_machine_learning(Card):
    CARD_KEY="T_Card_Ico_machine_learning"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_machine_learning_effect1)

class tT_Card_Ico_machine_learning_effect1(Effect):
    effType = EFF_TYPE.trigger

    observeSignals = (LOCATION.spellTrapZone, [Signal.StandbyPhase])

    AI_HINT = [AI_HINT.drawCard]
    AI_POWER = 1

    def y_cost(self, justCheck:bool, signal):
        if not isSignal(signal, Signal.StandbyPhase):
            return
        if self.game.whoseTurn != self.getSide():
            return
        if not self.getDeckLeftNum():
            return
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        yield self.y_drawCard(self.getSide(), 1)
