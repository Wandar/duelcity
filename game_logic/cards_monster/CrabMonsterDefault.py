# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Tiny Crab
卡名:迷你螃蟹
效果:1T:<被战斗破坏后>:从卡组把1只等级1的水族怪兽以守备表示特殊召唤。
"""

class CrabMonsterDefault(Card):
    CARD_KEY = 'CrabMonsterDefault'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(CrabMonsterDefault_e1)


class CrabMonsterDefault_e1(Effect):
    # 1T:<被战斗破坏后>:从卡组把1只等级1的水族怪兽以守备表示特殊召唤。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.grave, [Signal.DestroyedByBattle])
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 2

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.DestroyedByBattle, self.owner):
            return False
        def isT(c):
            return c.race == RACE.AQUA and c.level == 1
        targets = self.searchCards(LOCATION.deck, self.getSide(), CARD_TYPE.monster, self, isT)
        if not targets:
            return False
        if self.freeMonsterSpace() == 0:
            return False
        if justCheck:
            return True
        chosen = yield self.y_select1Card(targets, TITLE.specialSummon, canCancel=True)
        if not chosen:
            return False
        self.saveTarget1(chosen)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1(checkLocationChange=False)
        if not t:
            return False
        yield self.y_specialSummon(t, form=FORM.defence)
        return True

