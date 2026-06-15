# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Cryomancer5  【魔法】
卡图:深蓝背景,两段蓝白冰链相互咬合,其中一环正碎裂发光,冰封锁链被打破。
效果(AOTIP):
1A:打破冰封——以自己墓地1只怪兽为对象,该怪兽以攻击表示特殊召唤,其{ATK}+500。
"""

class tT_Cryomancer5(Card):
    CARD_KEY = "T_Cryomancer5"
    AUTHOR = "Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Cryomancer5_eff)

class tT_Cryomancer5_eff(Effect):
    effType = EFF_TYPE.active
    activateLocation = LOCATION.spellTrapZone
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 3

    def y_cost(self, justCheck: bool, signal):
        if not self.freeMonsterSpace(): return False
        graveMons = self.searchCards(LOCATION.grave, self.getSide(), CARD_TYPE.monster, self)
        if not graveMons: return False
        if justCheck: return True
        t = yield self.y_select1Card(graveMons, TITLE.specialSummon, self.getSide(), canCancel=True)
        if not t: return False
        self.saveTarget1(t)
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck: return True
        t = self.getLegalTarget1()
        if t and self.freeMonsterSpace():
            successNum = yield self.y_specialSummon(t, self.getSide(), FORM.attack)
            if successNum and t.isMonsterOnField():
                yield self.y_addCardData(t, attackAdd=500)
        return True
