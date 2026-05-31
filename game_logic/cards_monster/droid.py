# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Salvage Droid
卡名:回收机兵
"""

class droid(Card):
    CARD_KEY = "droid"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(droid_SalvageProtocol)



"""
1A:<场上效果>:自己场上存在的5星以上的植物族怪兽被破坏的场合，墓地存在的这张卡可以在自己场上特殊召唤。
1OT:<Graveyard effect>: When a Level 5 or higher MACHINE monster you control is destroyed, Special Summon this card.
"""
class droid_SalvageProtocol(Effect):
    effType = EFF_TYPE.optionalTrigger

    observeSignals = (LOCATION.grave, [Signal.Destroyed])

    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 3

    def y_cost(self, justCheck: bool, signal):
        if not isSignal(signal, Signal.Destroyed):
            return False
        if self.owner.location != LOCATION.grave:
            return False
        card = signal.card
        if card is None or card == self.owner:
            return False
        if card.side != self.getSide():
            return False
        if card.race != RACE.MACHINE:
            return False
        if card.level < 5:
            return False
        if self.freeMonsterSpace() == 0:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck:
            return True
        yield self.y_specialSummon(self.owner)
        return True
