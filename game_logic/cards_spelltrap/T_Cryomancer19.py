# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Cryomancer19  【永续魔法】
卡图:蓝色冰雪背景,由冰晶构成的华丽蓝白色装甲胸甲/宝座,对称设计。
效果(AOTIP):
1P:只要此卡在魔陷区,自己场上所有怪兽的{DEF}+800(冰晶宝座护甲领域)。
"""

class tT_Cryomancer19(Card):
    CARD_KEY = "T_Cryomancer19"
    AUTHOR = "Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Cryomancer19_eff)

class tT_Cryomancer19_eff(Effect):
    effType = EFF_TYPE.permanent
    observeSignals = (LOCATION.spellTrapZone, [
        Signal.AttachMonsterZone, Signal.DetachMonsterZone,
        Signal.AttachSpellZone, Signal.DetachSpellZone,
    ])
    uniID = 0

    def y_signal(self, signal):
        if not self.uniID:
            self.uniID = self.game.genUniID()
        myMons = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self)
        if myMons:
            yield self.y_removeBuffEffectSource(myMons, self.uniID)
        if self.owner.isInSpellZone() and myMons:
            yield self.y_addCardData(myMons, defenceAdd=800,
                                     effDuration=EFF_DURATION.fromSource, uniqueSourceID=self.uniID)
