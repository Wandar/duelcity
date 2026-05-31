# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_blood_link
卡名:血之羁绊
"""

#########################my

"""
1P:只要自己场上存在恶魔族怪兽,自己每次受到战斗伤害时回复等量基本分
"""

class tT_Card_Ico_blood_link(Card):
    CARD_KEY="T_Card_Ico_blood_link"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_blood_link_effect1)

class tT_Card_Ico_blood_link_effect1(Effect):
    effType = EFF_TYPE.permanent

    observeSignals = (LOCATION.spellTrapZone, [Signal.PlayerLPLoseByBattle])

    AI_HINT = [AI_HINT.enhance]
    AI_POWER = 1

    def y_cost(self, justCheck:bool, signal):
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck:bool, signal: Signal.PlayerLPLoseByBattle):
        if justCheck:
            return True
        if not isSignal(signal, Signal.PlayerLPLoseByBattle):
            return
        if signal.receiverPlayer != self.getSide():
            return
        def f(c):
            return c.race == RACE.FIEND
        demons = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self, f)
        if demons:
            yield self.y_healPlayer(self.getSide(), signal.lpLose)
