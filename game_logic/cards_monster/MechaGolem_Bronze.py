# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Acient Bronze Mech
卡名:古代青铜机械
"""

class MechaGolem_Bronze(Card):
    CARD_KEY="MechaGolem_Bronze"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(MechaGolem_Bronze_e1)


"""
1T:<除外区效果:自己的机械族怪兽被破坏时>:把此卡以守备表示特殊召唤。
"""
class MechaGolem_Bronze_e1(Effect):
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.banish, [Signal.Destroyed])
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 2

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Destroyed):
            return False
        if self.owner.location != LOCATION.banish:
            return False
        card = signal.card
        if card is None or card == self.owner:
            return False
        if card.side != self.getSide():
            return False
        if card.race != RACE.MACHINE:
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
