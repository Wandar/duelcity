# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Shaman11  【陷阱】
卡图:深绿萤火背景,黑色盔甲骑士站立,环绕绿色发光弯曲藤蔓,神秘自然魔力。
效果(AOTIP):
1OT:<对方怪兽宣告攻击时>:藤蔓缠缚——以攻击宣言的那只怪兽为对象,该回合其{ATK}-1000,并变为守备表示。
"""

class tT_Shaman11(Card):
    CARD_KEY = "T_Shaman11"
    AUTHOR = "Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Shaman11_eff)

class tT_Shaman11_eff(Effect):
    effType = EFF_TYPE.optionalTrigger
    observeSignals = (LOCATION.spellTrapZone, [Signal.RequestBattle])
    AI_HINT = [AI_HINT.debuff]
    EFF_POWER = 3

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
            yield self.y_addCardData(t, attackAdd=-1000,
                                     effDuration=EFF_DURATION.utilTurnEnds, uniqueSourceID=self.effUniID)
            yield self.y_changeForm(t, FORM.defence)
        return True
