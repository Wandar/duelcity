# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Fledgling Wings of Dawn
卡名:破晓之雏翼
效果:1T:自己的准备阶段:把场上的此卡送入弃牌区,从手牌·卡组把1只「破晓之翼」特殊召唤。
"""

class Fledgling(Card):
    CARD_KEY = 'Fledgling'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Fledgling_e1)


class Fledgling_e1(Effect):
    # 1T:自己的准备阶段:把场上的此卡送入弃牌区,从手牌·卡组把1只「破晓之翼」特殊召唤。
    effType = EFF_TYPE.optionalTrigger
    observeSignals = (LOCATION.monsterZone, [Signal.StandbyPhase])
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.StandbyPhase):
            return False
        if self.game.whoseTurn != self.getSide():
            return False
        if not self.owner.isMonsterOnField():
            return False
        def isTarget(c):
            return c.cardKey == "littleBird"
        targets = self.searchCards(LOCATION.hand | LOCATION.deck, self.getSide(), CARD_TYPE.monster, self, isTarget)
        if not targets:
            return False
        if justCheck:
            return True
        chosen = yield self.y_select1Card(targets, TITLE.specialSummon, canCancel=True)
        if not chosen:
            return False
        yield self.y_sendCardToGrave(self.owner)
        self.saveTarget1(chosen)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1(checkLocationChange=False)
        if not t:
            return False
        if self.freeMonsterSpace() == 0:
            return False
        yield self.y_specialSummon(t)
        return True

