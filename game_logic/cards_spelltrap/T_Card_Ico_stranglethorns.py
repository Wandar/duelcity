# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_stranglethorns
卡名:绞杀荆棘
"""

#########################my

"""
1I:对方怪兽攻击宣言时,使场上所有怪兽变为守备表示
"""

class tT_Card_Ico_stranglethorns(Card):
    CARD_KEY="T_Card_Ico_stranglethorns"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_stranglethorns_effect1)

class tT_Card_Ico_stranglethorns_effect1(Effect):
    effType = EFF_TYPE.optionalInstant

    observeSignals = (LOCATION.spellTrapZone, [Signal.InBattle])

    AI_HINT = [AI_HINT.eraser]
    AI_POWER = 1

    def y_cost(self, justCheck:bool, signal):
        if not (isSignal(signal, Signal.InBattle) and signal.attackerCard.side in self.getEnemySideTuple()):
            return
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        allMon = self.searchCards(LOCATION.monsterZone, -1, CARD_TYPE.monster, self)
        for m in allMon:
            yield self.y_changeForm(m, FORM.defence)
