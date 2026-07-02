# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:ghostdrink
卡名:ghostdrink
"""
"""
1A:选择场上一只怪兽{ATK}加500,回合结束时该怪兽受到1000点伤害
"""
class tghostdrink(Card):
    CARD_KEY="ghostdrink"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tghostdrink_effect1)

class tghostdrink_effect1(Effect):
    effType = EFF_TYPE.active

    observeSignals = (LOCATION.grave, [Signal.TurnEnds])

    AI_HINT = [AI_HINT.addAtk]
    AI_POWER = 1

    _targetUniID = -1

    def y_cost(self, justCheck:bool, signal):
        if isSignal(signal, Signal.TurnEnds):
            return False
        targets = self.searchCards(LOCATION.monsterZone, -1, CARD_TYPE.monster, self)
        if not targets:
            return False
        if justCheck:
            return True
        target = yield self.y_select1Card(targets, TITLE.target, canCancel=True)
        if target:
            self.saveTarget1(target)
            return True

    def y_activate(self, justCheck:bool, signal):
        if isSignal(signal, Signal.TurnEnds):
            target = self.getLegalTarget1()
            if target and target.isOnField():
                yield self.y_addCardData(target, attackAdd=-1000, defenceAdd=-1000,
                                         effDuration=EFF_DURATION.utilTurnEnds)
            return True

        if justCheck:
            return True
        target = self.getLegalTarget1()
        if target:
            yield self.y_addCardData(target, attackAdd=500, effDuration=EFF_DURATION.utilTurnEnds)
        return True
