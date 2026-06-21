# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_force_field  【陷阱】
卡图:蓝紫背景,多道蓝白光束汇聚击打青色球体,力场防护。
效果(AOTIP):
1OT:<对方怪兽攻击宣言时>:把该攻击怪兽返回持有者手牌。
"""

class tT_Card_Ico_force_field(Card):
    CARD_KEY = "T_Card_Ico_force_field"
    AUTHOR = "Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_force_field_eff)

class tT_Card_Ico_force_field_eff(Effect):
    # 1OT:<对方怪兽攻击宣言时>:把该攻击怪兽返回持有者手牌。
    effType = EFF_TYPE.optionalTrigger
    observeSignals = (LOCATION.spellTrapZone, [Signal.RequestBattle])
    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 4

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
        if not t:
            return False
        yield self.y_returnCardToHand(t)
        return True
