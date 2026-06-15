# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:thegolem  【魔法】
卡图:蓝灰背景,巨大土黄石质魔像(骷髅面孔蓝眼)张臂站立,缠绕蓝色闪电,法师对峙。
效果(AOTIP):
1A:以自己场上1只怪兽为对象,赋予磐石之躯——该怪兽{DEF}+1000,且不再受到战斗伤害。
"""

class tthegolem(Card):
    CARD_KEY = "thegolem"
    AUTHOR = "Unnamed"
    def effectsInit(self):
        self.initEffect(tthegolem_eff)

class tthegolem_eff(Effect):
    effType = EFF_TYPE.active
    activateLocation = LOCATION.spellTrapZone
    AI_HINT = [AI_HINT.enhance]
    EFF_POWER = 3

    def y_cost(self, justCheck: bool, signal):
        myMons = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self)
        if not myMons: return False
        if justCheck: return True
        t = yield self.y_select1Card(myMons, TITLE.target, self.getSide(), canCancel=True)
        if not t: return False
        self.saveTarget1(t)
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck: return True
        t = self.getLegalTarget1()
        if t and t.isMonsterOnField():
            yield self.y_addCardData(t, defenceAdd=1000, uniqueSourceID=self.effUniID)
            yield self.y_addImmunityBuffToCard(t, IMMUNITY_MASK.battleDamage,
                                               EFF_DURATION.onceForever, self.effUniID)
        return True
