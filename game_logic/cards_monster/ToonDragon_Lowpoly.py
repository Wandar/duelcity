# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Sproutling Sky Dragon
卡名:豆芽小飞龙
"""

class ToonDragon_Lowpoly(Card):
    CARD_KEY = "ToonDragon_Lowpoly"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(ToonDragon_Lowpoly_ElementalChorus)


"""
1P:<场上效果>:场上的炎属性怪兽的攻击力上升500，水属性怪兽的攻击力下降400。
1P: <While on the field>: All FIRE monsters on the field gain 500 ATK; all WATER monsters on the field lose 400 ATK.
"""
class ToonDragon_Lowpoly_ElementalChorus(Effect):
    effType = EFF_TYPE.permanent

    observeSignals = (LOCATION.monsterZone, [
        Signal.AttachMonsterZone,
        Signal.DetachMonsterZone,
        Signal.CardAttrChanged,
    ])

    AI_HINT = [AI_HINT.permanent, AI_HINT.addAtk]
    EFF_POWER = 3

    def y_signal(self, signal):
        # 此卡离场：清除所有加成
        if isSignal(signal, Signal.DetachMonsterZone, self.owner):
            allCards = self.searchCards(LOCATION.mask_all, -1, CARD_TYPE.all, None)
            yield self.y_removeBuffEffectSource(allCards, self.effUniID)
            return

        # 其他怪兽离场：移除对它的加成
        if isSignal(signal, Signal.DetachMonsterZone):
            yield self.y_removeBuffEffectSource(signal.card, self.effUniID)
            return

        if not self.owner.isMonsterOnField():
            return

        def isFire(card):
            return card.attr == ATTR.FIRE

        def isWater(card):
            return card.attr == ATTR.WATER

        fireMonsters = self.searchCards(
            LOCATION.monsterZone, -1, CARD_TYPE.monster, None, isFire
        )
        waterMonsters = self.searchCards(
            LOCATION.monsterZone, -1, CARD_TYPE.monster, None, isWater
        )

        if fireMonsters:
            yield self.y_addCardData(
                fireMonsters,
                attackAdd=500,
                effDuration=EFF_DURATION.fromSource,
                uniqueSourceID=self.effUniID,
            )
        if waterMonsters:
            yield self.y_addCardData(
                waterMonsters,
                attackAdd=-400,
                effDuration=EFF_DURATION.fromSource,
                uniqueSourceID=self.effUniID,
            )
