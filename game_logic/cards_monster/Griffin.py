# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Giant Griffin
卡名:大狮鹫
"""

class Griffin(Card):
    CARD_KEY = "Griffin"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Griffin_GuardianFeathers)


"""
1P:<场上效果>:我方场上所有风属性怪兽（包含此卡）攻击力+300
1P:<While this card is in the Monster Zone>:All WIND monsters on your field (including this card) gain +300 ATK. Remove this effect when this card leaves the field.
"""
class Griffin_GuardianFeathers(Effect):
    effType = EFF_TYPE.permanent

    observeSignals = (LOCATION.monsterZone, [
        Signal.AttachMonsterZone,
        Signal.DetachMonsterZone,
        Signal.CardAttrChanged,
    ])

    AI_HINT = [AI_HINT.permanent, AI_HINT.addAtk]
    EFF_POWER = 3

    def y_signal(self, signal):
        # 此卡离场：移除所有由本效果施加的ATK加成
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

        def isWind(card):
            return card.attr == ATTR.WIND

        windMonsters = self.searchCards(
            LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, None, isWind
        )
        if not windMonsters:
            return

        yield self.y_addCardData(
            windMonsters,
            attackAdd=300,
            effDuration=EFF_DURATION.fromSource,
            uniqueSourceID=self.effUniID,
        )
