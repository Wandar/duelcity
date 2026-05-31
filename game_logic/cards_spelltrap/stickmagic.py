# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:stickmagic
卡名:stickmagic
"""
"""
1A:从手牌特殊召唤一只LV4以下的怪兽,回合结束时从墓地特殊召唤一只LV4以下的怪兽
"""
class tstickmagic(Card):
    CARD_KEY="stickmagic"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tstickmagic_effect1)

class tstickmagic_effect1(Effect):
    effType = EFF_TYPE.active

    observeSignals = (LOCATION.grave, [Signal.TurnEnds])

    AI_HINT = [AI_HINT.summoner]
    AI_POWER = 3

    _activatedTurn = -1

    def y_cost(self, justCheck:bool, signal):
        if isSignal(signal, Signal.TurnEnds):
            return False
        handMonsters = self.searchCards(LOCATION.hand, self.getSide(), CARD_TYPE.monster, self,
                                         lambda c: c.level <= 4 and c.canSpecialSummon())
        if not handMonsters:
            return False
        if justCheck:
            return True
        target = yield self.y_select1Card(handMonsters, TITLE.specialSummon, canCancel=True)
        if target:
            self.saveTarget1(target)
            return True

    def y_activate(self, justCheck:bool, signal):
        if isSignal(signal, Signal.TurnEnds):
            if self._activatedTurn == self.game.curTurn:
                graveMonsters = self.searchCards(LOCATION.grave, self.getSide(), CARD_TYPE.monster,
                                                  self, lambda c: c.level <= 4
                                                                  and c.canSpecialSummon())
                if graveMonsters:
                    target = yield self.y_select1Card(graveMonsters, TITLE.specialSummon,
                                                       canCancel=True)
                    if target:
                        yield self.y_specialSummon(target)
            return True

        if justCheck:
            return True
        target = self.getLegalTarget1()
        if target:
            yield self.y_specialSummon(target)
            self._activatedTurn = self.game.curTurn
        return True
