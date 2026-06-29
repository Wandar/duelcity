# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Bunny Rat
卡名:雪兔
效果:1P:我方场上其他兽族怪兽攻击力·守备力上升200。
"""

class BunnyRat(Card):
    CARD_KEY = 'BunnyRat'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(BunnyRat_e1)


class BunnyRat_e1(Effect):
    # 1P:我方场上其他兽族怪兽攻击力·守备力上升200。
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
            yield self.y_addCardData(targets, attackAdd=200, defenceAdd=200,
                                     effDuration=EFF_DURATION.fromSource, uniqueSourceID=self.effUniID)
