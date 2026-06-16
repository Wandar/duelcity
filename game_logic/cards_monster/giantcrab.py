# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Giant Crab
卡名:巨蟹
效果:1P:场上所有非水属性怪兽的攻击力和防御力都-300。
"""

class giantcrab(Card):
    CARD_KEY = 'giantcrab'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(giantcrab_e1)


class giantcrab_e1(Effect):
    # 1P:场上所有非水属性怪兽的攻击力和防御力都-300。
    effType = EFF_TYPE.permanent
    observeSignals = (LOCATION.monsterZone, [Signal.AttachMonsterZone, Signal.DetachMonsterZone, Signal.CardAttrChanged])
    AI_HINT = [AI_HINT.permanent, AI_HINT.debuff]
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
        def isNonWater(c):
            return c.attr != ATTR.WATER
        targets = self.searchCards(LOCATION.monsterZone, -1, CARD_TYPE.monster, None, isNonWater)
        if targets:
            yield self.y_addCardData(targets, attackAdd=-300, defenceAdd=-300,
                                     effDuration=EFF_DURATION.fromSource, uniqueSourceID=self.effUniID)

