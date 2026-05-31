# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_Impervious
卡名:坚不可摧
"""

#########################my

"""
1I:本回合自己场上的怪兽不会被战斗或效果破坏
"""

class tT_Card_Ico_Impervious(Card):
    CARD_KEY="T_Card_Ico_Impervious"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_Impervious_effect1)

class tT_Card_Ico_Impervious_effect1(Effect):
    effType = EFF_TYPE.optionalInstant

    observeSignals = (LOCATION.spellTrapZone, [Signal.InBattle])

    AI_HINT = [AI_HINT.enhance]
    AI_POWER = 1

    def y_cost(self, justCheck:bool, signal):
        myMon = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self)
        if not myMon:
            return
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        myMon = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self)
        for m in myMon:
            yield self.y_addImmunityBuffToCard(m, IMMUNITY_MASK.destroyByBattle | IMMUNITY_MASK.destroyByEffect,
                                                EFF_DURATION.utilTurnEnds, self.uniID)
