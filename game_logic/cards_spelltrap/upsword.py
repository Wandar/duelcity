# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:upsword  【永续魔法】
卡图:蓝色背景,银白色长剑竖立中央,周围五个青蓝色向上箭头,攻击力提升/武器强化。
效果(AOTIP):
1P:只要此卡在魔陷区,自己场上所有怪兽的{ATK}+400(扬剑增幅领域)。
"""

class tupsword(Card):
    CARD_KEY = "upsword"
    AUTHOR = "Unnamed"
    def effectsInit(self):
        self.initEffect(tupsword_eff)

class tupsword_eff(Effect):
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
            yield self.y_addCardData(myMons, attackAdd=400,
                                     effDuration=EFF_DURATION.fromSource, uniqueSourceID=self.uniID)
