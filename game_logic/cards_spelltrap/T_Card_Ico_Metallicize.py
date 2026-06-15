# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_Metallicize  【永续魔法】
卡图:蓝色背景,披风人物周围漂浮多件蓝色发光金属物,金属化转变。
效果(AOTIP):
1P:只要此卡在魔陷区,自己场上所有怪兽的{DEF}+500(金属护层领域,固定不叠加)。
"""

class tT_Card_Ico_Metallicize(Card):
    CARD_KEY = "T_Card_Ico_Metallicize"
    AUTHOR = "Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_Metallicize_eff)

class tT_Card_Ico_Metallicize_eff(Effect):
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
            yield self.y_addCardData(myMons, defenceAdd=500,
                                     effDuration=EFF_DURATION.fromSource, uniqueSourceID=self.uniID)
