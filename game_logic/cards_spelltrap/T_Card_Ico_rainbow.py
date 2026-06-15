# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_rainbow  【永续魔法】
卡图:棕红背景,橙狐与棕刺猬奔跑,上方彩虹文字云朵,下方蓝色冰晶,色彩活泼。
效果(AOTIP):
1P:自己场上的怪兽每存在1种不同的属性,自己场上所有怪兽的{ATK}各+300(七彩共鸣)。
"""

class tT_Card_Ico_rainbow(Card):
    CARD_KEY = "T_Card_Ico_rainbow"
    AUTHOR = "Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_rainbow_eff)

class tT_Card_Ico_rainbow_eff(Effect):
    effType = EFF_TYPE.permanent
    observeSignals = (LOCATION.spellTrapZone, [
        Signal.AttachMonsterZone, Signal.DetachMonsterZone,
        Signal.AttachSpellZone, Signal.DetachSpellZone, Signal.CardAttrChanged,
    ])
    uniID = 0

    def y_signal(self, signal):
        if not self.uniID:
            self.uniID = self.game.genUniID()
        myMons = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self)
        if myMons:
            yield self.y_removeBuffEffectSource(myMons, self.uniID)
        if self.owner.isInSpellZone() and myMons:
            attrs = set(c.attr for c in myMons if c.attr)
            bonus = len(attrs) * 300
            if bonus > 0:
                yield self.y_addCardData(myMons, attackAdd=bonus,
                                         effDuration=EFF_DURATION.fromSource, uniqueSourceID=self.uniID)
