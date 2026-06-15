# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Cryomancer9  【魔法】
卡图:深蓝背景,蓝白光束斜穿画面,散落发光冰晶碎片,冰霜射线爆裂。
效果(AOTIP):
1A:冰霜射线——以对方场上1只怪兽为对象,对它造成1000伤害;若它因此被破坏,
   射线贯穿,对对方造成500伤害。
"""

class tT_Cryomancer9(Card):
    CARD_KEY = "T_Cryomancer9"
    AUTHOR = "Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Cryomancer9_eff)

class tT_Cryomancer9_eff(Effect):
    effType = EFF_TYPE.active
    activateLocation = LOCATION.spellTrapZone
    AI_HINT = [AI_HINT.damager]
    EFF_POWER = 3

    def y_cost(self, justCheck: bool, signal):
        enMons = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self)
        if not enMons: return False
        if justCheck: return True
        t = yield self.y_select1Card(enMons, TITLE.target, self.getSide(), canCancel=True)
        if not t: return False
        self.saveTarget1(t)
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck: return True
        t = self.getLegalTarget1()
        if not t: return False
        yield self.y_damageCard(t, 1000)
        if not t.isMonsterOnField():
            yield self.y_damagePlayer(self.getEnemySideTuple(), 500)
        return True
