# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_skim
卡名:掠夺操控
"""

#########################my

"""
1I:对方特殊召唤机械族怪兽时,获得其控制权直到结束阶段
"""

class tT_Card_Ico_skim(Card):
    CARD_KEY="T_Card_Ico_skim"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_skim_effect1)

class tT_Card_Ico_skim_effect1(Effect):
    effType = EFF_TYPE.optionalInstant

    observeSignals = (LOCATION.spellTrapZone, [Signal.SpecialSummon])

    AI_HINT = [AI_HINT.eraser]
    AI_POWER = 1

    def y_cost(self, justCheck:bool, signal):
        if not isSignal(signal, Signal.SpecialSummon):
            return
        card = getattr(signal, 'card', None)
        if not card or card.side not in self.getEnemySideTuple():
            return
        if card.race != RACE.MACHINE:
            return
        if justCheck:
            return True
        self.saveTarget1(card)
        return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        target = self.getLegalTarget1()
        if target:
            yield self.y_changeMonsterController(target, self.getSide(), EFF_DURATION.utilTurnEnds, self.uniID)
