# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_Obsidian_Skin  【陷阱】
卡图:紫红背景,全身覆盖黑紫岩石尖刺的魔化人形,红色眼睛发光。
效果(AOTIP):
1OT:<自己怪兽被攻击时>:以攻击的怪兽为对象,黑曜尖刺反弹,对它造成800伤害。
"""

class tT_Card_Ico_Obsidian_Skin(Card):
    CARD_KEY = "T_Card_Ico_Obsidian_Skin"
    AUTHOR = "Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_Obsidian_Skin_eff)

class tT_Card_Ico_Obsidian_Skin_eff(Effect):
    effType = EFF_TYPE.optionalTrigger
    observeSignals = (LOCATION.spellTrapZone, [Signal.RequestBattle])
    AI_HINT = [AI_HINT.damager]
    EFF_POWER = 3

    def y_cost(self, justCheck: bool, signal):
        if not isSignal(signal, Signal.RequestBattle): return False
        recv = signal.receiverCard
        atkCard = signal.attackerCard
        if recv is None or not self.checkAlly(recv): return False
        if atkCard is None: return False
        if justCheck: return True
        self.saveTarget1(atkCard)
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck: return True
        atk = self.getLegalTarget1()
        if atk and atk.isMonsterOnField():
            yield self.y_damageCard(atk, 800)
        return True
