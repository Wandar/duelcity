# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Soul War Tiger
卡名:灵魂战虎
效果:1T:<被破坏后>:发现一张等级6以下的兽族怪兽并特殊召唤。2P:我方场上其他兽族怪兽攻击力·守备力上升400。
"""

class GhostTiger(Card):
    CARD_KEY = "GhostTiger"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(GhostTiger_e1)
        self.initEffect(GhostTiger_e2)


class GhostTiger_e1(Effect):
    # 1T:<被破坏后>:发现一张等级6以下的兽族怪兽并特殊召唤。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.grave, [Signal.Destroyed])
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 4

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Destroyed, self.owner):
            return False
        if self.freeMonsterSpace() == 0:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        picked = yield self.y_discoverCard(title=TITLE.specialSummon, side=self.getSide(), race=RACE.BEAST,
                                           cardType=CARD_TYPE.monster, maxLevel=6, count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked)
        return True


class GhostTiger_e2(Effect):
    # 2P:我方场上其他兽族怪兽攻击力·守备力上升400。
    effType = EFF_TYPE.permanent
    observeSignals = (LOCATION.monsterZone, [Signal.AttachMonsterZone, Signal.DetachMonsterZone, Signal.CardRaceChanged])
    AI_HINT = [AI_HINT.permanent, AI_HINT.enhance]
    EFF_POWER = 3

    def y_signal(self, signal):
        if isSignal(signal, Signal.DetachMonsterZone, self.owner):
            allCards = self.searchCards(LOCATION.mask_all, -1, CARD_TYPE.all, None)
            yield self.y_removeBuffEffectSource(allCards, self.effUniID)
            return
        if isSignal(signal, Signal.DetachMonsterZone):
            yield self.y_removeBuffEffectSource(signal.card, self.effUniID)
            return
        if not self.owner.isMonsterOnField():
            return
        def isOtherBeast(c):
            return c != self.owner and c.race == RACE.BEAST
        targets = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, None, isOtherBeast)
        if targets:
            yield self.y_addCardData(targets, attackAdd=400, defenceAdd=400,
                                     effDuration=EFF_DURATION.fromSource, uniqueSourceID=self.effUniID)
