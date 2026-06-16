# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Armored Stone Golem
卡名:重甲石傀儡
效果:1T:<召唤时>:从卡组把1只等级2以下的岩石族·机械族以守备表示特殊召唤。
"""

class SKM_Iron_Golem(Card):
    CARD_KEY = 'SKM_Iron_Golem'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(SKM_Iron_Golem_e1)


class SKM_Iron_Golem_e1(Effect):
    # 1T:<召唤时>:从卡组把1只等级2以下的岩石族·机械族以守备表示特殊召唤。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        def isTarget(c):
            return c.level <= 2 and c.race in (RACE.ROCK, RACE.MACHINE)
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

