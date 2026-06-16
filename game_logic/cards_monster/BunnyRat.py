# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Bunny Rat
卡名:雪兔
效果:1T:自己回合结束时,此卡在场上的场合,从卡组把1只「雪兔」特殊召唤。
"""

class BunnyRat(Card):
    CARD_KEY = 'BunnyRat'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(BunnyRat_e1)


class BunnyRat_e1(Effect):
    # 1T:自己回合结束时,此卡在场上的场合,从卡组把1只「雪兔」特殊召唤。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.TurnEnds])
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.TurnEnds):
            return False
        if self.game.whoseTurn != self.getSide():
            return False
        if not self.owner.isMonsterOnField():
            return False
        def isTarget(c):
            return c.cardKey == "BunnyRat"
        targets = self.searchCards(LOCATION.deck, self.getSide(), CARD_TYPE.monster, self, isTarget)
        if not targets:
            return False
        if self.freeMonsterSpace() == 0:
            return False
        if justCheck:
            return True
        self.saveTarget1(targets[0])
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1(checkLocationChange=False)
        if not t:
            return False
        yield self.y_specialSummon(t)
        return True

