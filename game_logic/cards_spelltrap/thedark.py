# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:thedark  【永续魔法】
卡图:紫色渐变背景,中央深邃漩涡黑色虚空,周围粉紫云雾与蓝紫流光,暗黑次元入口。
效果(AOTIP):
1P:只要此卡在魔陷区,自己场上的暗属性怪兽的{ATK}+500(暗黑次元主宰)。
"""

class tthedark(Card):
    CARD_KEY = "thedark"
    AUTHOR = "Unnamed"
    def effectsInit(self):
        self.initEffect(tthedark_eff)

class tthedark_eff(Effect):
    effType = EFF_TYPE.permanent
    observeSignals = (LOCATION.spellTrapZone, [
        Signal.AttachMonsterZone, Signal.DetachMonsterZone,
        Signal.AttachSpellZone, Signal.DetachSpellZone, Signal.CardAttrChanged,
    ])
    uniID = 0

    def _isDark(self, c):
        return c.attr == ATTR.DARK

    def y_signal(self, signal):
        if not self.uniID:
            self.uniID = self.game.genUniID()
        darks = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self, self._isDark)
        if darks:
            yield self.y_removeBuffEffectSource(darks, self.uniID)
        if self.owner.isInSpellZone() and darks:
            yield self.y_addCardData(darks, attackAdd=500,
                                     effDuration=EFF_DURATION.fromSource, uniqueSourceID=self.uniID)
