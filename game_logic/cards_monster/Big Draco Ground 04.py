# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Ironback Dragon Turtle
卡名:重壳巨龙龟
效果:1P:守备表示的此卡不会被战斗破坏。2T:<被效果破坏时>:从卡组把1只等级3以下的龙族特殊召唤。
"""

class Big_Draco_Ground_04(Card):
    CARD_KEY = 'Big Draco Ground 04'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Big_Draco_Ground_04_e1)
        self.initEffect(Big_Draco_Ground_04_e2)


class Big_Draco_Ground_04_e1(Effect):
    # 1P:守备表示的此卡不会被战斗破坏。
    # NOTE: "守备不被战斗破坏" 暂无钩子,登记为常驻标记效果,待战斗结算查询。
    effType = EFF_TYPE.permanent
    observeSignals = (LOCATION.monsterZone, [Signal.AttachMonsterZone, Signal.DetachMonsterZone])
    AI_HINT = [AI_HINT.permanent]
    EFF_POWER = 3

    def y_signal(self, signal):
        return
        yield


class Big_Draco_Ground_04_e2(Effect):
    # 2T:<被效果破坏时>:从卡组把1只等级3以下的龙族特殊召唤。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.grave, [Signal.DestroyedByEffect])
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.DestroyedByEffect, self.owner):
            return False
        def isTarget(c):
            return c.race == RACE.DRAGON and c.level <= 3
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
        yield self.y_specialSummon(t)
        return True

