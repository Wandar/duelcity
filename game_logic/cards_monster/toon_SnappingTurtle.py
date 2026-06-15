# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Slow-Slow Little Turtle
卡名:慢慢小龟
"""

class toon_SnappingTurtle(Card):
    CARD_KEY="toon_SnappingTurtle"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(toon_SnappingTurtle_e1)


"""
1T:此卡召唤后的第2个自己准备阶段:自己抽2张卡。
"""
class toon_SnappingTurtle_e1(Effect):
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.StandbyPhase])
    AI_HINT = [AI_HINT.drawCard]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.StandbyPhase):
            return False
        if self.game.whoseTurn != self.getSide():
            return False
        # summonedTurn is set on summon; my standby phases land on summonedTurn+2 (1st)
        # and summonedTurn+4 (2nd) since curTurn advances by 1 each player-turn
        if self.owner.summonedTurn == 0:
            return False
        if self.game.curTurn != self.owner.summonedTurn + 4:
            return False
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        yield self.y_drawCard(self.getSide(), 2)
        return True
