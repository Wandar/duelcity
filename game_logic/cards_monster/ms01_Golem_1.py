# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Tiny Stone Golem
卡名:石头小傀儡
"""

class ms01_Golem_1(Card):
    CARD_KEY="ms01_Golem_1"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(ms01_Golem_1_e1)


"""
1T:<墓地效果:自己的岩石族怪兽被破坏时>:把此卡以守备表示特殊召唤。
"""
class ms01_Golem_1_e1(Effect):
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.grave, [Signal.Destroyed])
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 2

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Destroyed):
            return False
        if self.owner.location != LOCATION.grave:
            return False
        card = signal.card
        if card is None or card == self.owner:
            return False
        if card.side != self.getSide():
            return False
        if card.race != RACE.ROCK:
            return False
        if self.freeMonsterSpace() == 0:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        yield self.y_specialSummon(self.owner, form=FORM.defence)
        return True
