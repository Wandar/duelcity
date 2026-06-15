# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Dragonknight14  【永续魔法】
卡图:深蓝紫背景,黑色大型龙头颈特写,鳞片蓝紫发光,龙骑士坐骑。
效果(AOTIP):
1P:只要此卡在魔陷区,自己墓地每有1只龙族怪兽,自己场上所有怪兽的{ATK}各+200(龙主威严)。
"""

class tT_Dragonknight14(Card):
    CARD_KEY = "T_Dragonknight14"
    AUTHOR = "Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Dragonknight14_eff)

class tT_Dragonknight14_eff(Effect):
    effType = EFF_TYPE.permanent
    observeSignals = (LOCATION.spellTrapZone, [
        Signal.AttachMonsterZone, Signal.DetachMonsterZone,
        Signal.AttachSpellZone, Signal.DetachSpellZone,
        Signal.EnterGrave, Signal.LeaveGrave,
    ])
    uniID = 0

    def _isDragon(self, c):
        return c.race == RACE.DRAGON

    def y_signal(self, signal):
        if not self.uniID:
            self.uniID = self.game.genUniID()
        myMons = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self)
        if myMons:
            yield self.y_removeBuffEffectSource(myMons, self.uniID)
        if self.owner.isInSpellZone() and myMons:
            dragons = self.searchCards(LOCATION.grave, self.getSide(), CARD_TYPE.monster, self, self._isDragon)
            bonus = len(dragons) * 200
            if bonus > 0:
                yield self.y_addCardData(myMons, attackAdd=bonus,
                                         effDuration=EFF_DURATION.fromSource, uniqueSourceID=self.uniID)
