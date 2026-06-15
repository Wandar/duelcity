# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_Impervious  【陷阱】
卡图:蓝色放射光,人形剪影立于金黄三角光锥前,两侧黄色闪电,散发无敌光芒。
效果(AOTIP):
1OT:<自己怪兽被攻击时>:以那只被攻击的怪兽为对象,直到对方下个回合结束,
   该怪兽不受任何破坏与效果影响(刀枪不入)。
"""

class tT_Card_Ico_Impervious(Card):
    CARD_KEY = "T_Card_Ico_Impervious"
    AUTHOR = "Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_Impervious_eff)

class tT_Card_Ico_Impervious_eff(Effect):
    effType = EFF_TYPE.optionalTrigger
    observeSignals = (LOCATION.spellTrapZone, [Signal.RequestBattle])
    AI_HINT = [AI_HINT.enhance]
    EFF_POWER = 3

    def y_cost(self, justCheck: bool, signal):
        if not isSignal(signal, Signal.RequestBattle): return False
        recv = signal.receiverCard
        if recv is None or not recv.isMonsterOnField(): return False
        if not self.checkAlly(recv): return False
        if justCheck: return True
        self.saveTarget1(recv)
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck: return True
        t = self.getLegalTarget1()
        if t and t.isMonsterOnField():
            yield self.y_addImmunityBuffToCard(t, IMMUNITY_MASK.all,
                                               EFF_DURATION.utilNextTurnEnds, self.effUniID)
        return True
