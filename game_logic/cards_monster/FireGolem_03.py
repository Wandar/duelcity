# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Marsh Mud Giant
卡名:沼泽泥巨人
效果:1T:<被战斗破坏时>:从卡组把1只等级3以下的怪兽以守备表示特殊召唤。
"""

class FireGolem_03(Card):
    CARD_KEY = 'FireGolem_03'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(FireGolem_03_e1)


class FireGolem_03_e1(Effect):
    # 1T:<被战斗破坏时>:从卡组把1只等级3以下的怪兽以守备表示特殊召唤。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.grave, [Signal.DestroyedByBattle])
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.DestroyedByBattle, self.owner):
            return False
        def isTarget(c):
            return c.level <= 3
        targets = self.searchCards(LOCATION.deck, self.getSide(), CARD_TYPE.monster, self, isTarget)
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

