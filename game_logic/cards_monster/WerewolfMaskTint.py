# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Werewolf Mask
卡名:狼人面具
效果:1P:自己其他兽战士族怪兽攻击力+200。
"""

class WerewolfMaskTint(Card):
    CARD_KEY = 'WerewolfMaskTint'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(WerewolfMaskTint_e1)


class WerewolfMaskTint_e1(Effect):
    # 1P:自己其他兽战士族怪兽攻击力+200。
    effType = EFF_TYPE.permanent
    observeSignals = (LOCATION.monsterZone, [Signal.AttachMonsterZone, Signal.DetachMonsterZone, Signal.CardRaceChanged])
    AI_HINT = [AI_HINT.permanent, AI_HINT.addAtk]
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
        def isOther(c):
            return c != self.owner and c.race == RACE.BEASTWARRIOR
        targets = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, None, isOther)
        if targets:
            yield self.y_addCardData(targets, attackAdd=200,
                                     effDuration=EFF_DURATION.fromSource, uniqueSourceID=self.effUniID)

