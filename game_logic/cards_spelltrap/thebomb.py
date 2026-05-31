# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:thebomb
卡名:致命炸弹
"""

#########################my

"""
1I:对方召唤怪兽时,破坏该怪兽并对对方造成500伤害
"""

class tthebomb(Card):
    CARD_KEY="thebomb"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tthebomb_effect1)

class tthebomb_effect1(Effect):
    effType = EFF_TYPE.optionalInstant

    observeSignals = (LOCATION.spellTrapZone, [Signal.NormalSummon, Signal.SpecialSummon])

    AI_HINT = [AI_HINT.eraser]
    AI_POWER = 1

    enemy = 0
    def y_cost(self, justCheck:bool, signal):
        if not (isSignal(signal, Signal.NormalSummon) or isSignal(signal, Signal.SpecialSummon)):
            return
        card = getattr(signal, 'card', None)
        if not card or card.side not in self.getEnemySideTuple():
            return
        if justCheck:
            return True
        self.enemy = yield self.y_select1EnemySide()
        self.saveTarget1(card)
        return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        target = self.getLegalTarget1()
        if target:
            yield self.y_destroyCard(target)
        yield self.y_damagePlayer(self.enemy, 500)
