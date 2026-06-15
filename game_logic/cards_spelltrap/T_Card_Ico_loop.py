# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_loop  【魔法】
卡图:蓝色背景,中央金黄无限符号(∞)由橙色火焰描绘,无限循环。
效果(AOTIP):
1A:以自己场上1只怪兽为对象,这个回合该怪兽可以多攻击2次(无限连击)。
"""

class tT_Card_Ico_loop(Card):
    CARD_KEY = "T_Card_Ico_loop"
    AUTHOR = "Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_loop_eff)

class tT_Card_Ico_loop_eff(Effect):
    effType = EFF_TYPE.active
    activateLocation = LOCATION.spellTrapZone
    AI_HINT = [AI_HINT.battleBenefit]
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
            yield self.y_addCardData(t, attackTimesAdd=2,
                                     effDuration=EFF_DURATION.utilTurnEnds, uniqueSourceID=self.effUniID)
        return True
