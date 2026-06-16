# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Tri-Headed Dragon King
卡名:三首龙王
效果:1P:此卡1回合可攻击3次。
"""

class BattleDragon01(Card):
    CARD_KEY = 'BattleDragon01'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(BattleDragon01_e1)


class BattleDragon01_e1(Effect):
    # 1P:此卡1回合可攻击3次。
    effType = EFF_TYPE.permanent
    observeSignals = (LOCATION.monsterZone, [Signal.AttachMonsterZone, Signal.DetachMonsterZone])
    AI_HINT = [AI_HINT.permanent, AI_HINT.battleBenefit]
    EFF_POWER = 4

    def y_signal(self, signal):
        if isSignal(signal, Signal.DetachMonsterZone, self.owner):
            yield self.y_removeBuffEffectSource(self.owner, self.effUniID)
            return
        if not self.owner.isMonsterOnField():
            return
        yield self.y_changeCardData(self.owner, newAttackTimes=3,
                                    effDuration=EFF_DURATION.fromSource, uniqueSourceID=self.effUniID)

