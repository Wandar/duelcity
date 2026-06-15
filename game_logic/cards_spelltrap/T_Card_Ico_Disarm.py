# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_Disarm  【陷阱】
卡图:红橙爆裂背景,蓝灰弯刀与断裂长剑碎成数块,碎片四散。
效果(AOTIP):
1OT:<对方怪兽宣告攻击时>:武装崩裂——以攻击宣言的那只怪兽为对象,对它造成1000伤害。
"""

class tT_Card_Ico_Disarm(Card):
    CARD_KEY = "T_Card_Ico_Disarm"
    AUTHOR = "Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_Disarm_eff)

class tT_Card_Ico_Disarm_eff(Effect):
    effType = EFF_TYPE.optionalTrigger
    observeSignals = (LOCATION.spellTrapZone, [Signal.RequestBattle])
    AI_HINT = [AI_HINT.damager]
    EFF_POWER = 2

    def y_cost(self, justCheck: bool, signal):
        if not isSignal(signal, Signal.RequestBattle): return False
        atkCard = signal.attackerCard
        if atkCard is None or atkCard.side not in self.getEnemySideTuple(): return False
        if not atkCard.isMonsterOnField(): return False
        if justCheck: return True
        self.saveTarget1(atkCard)
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck: return True
        t = self.getLegalTarget1()
        if t and t.isMonsterOnField():
            yield self.y_damageCard(t, 1000)
        return True
