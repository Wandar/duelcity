# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_Made_In_Abyss  【魔法】
卡图:深紫背景,中央漆黑圆形深渊洞口,四周红光边缘碎片,深不见底的裂缝。
效果(AOTIP):
1A:深渊吞噬——把对方墓地的卡全部除外,每除外1张对对方造成200伤害。
"""

class tT_Card_Ico_Made_In_Abyss(Card):
    CARD_KEY = "T_Card_Ico_Made_In_Abyss"
    AUTHOR = "Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_Made_In_Abyss_eff)

class tT_Card_Ico_Made_In_Abyss_eff(Effect):
    effType = EFF_TYPE.active
    activateLocation = LOCATION.spellTrapZone
    AI_HINT = [AI_HINT.damager, AI_HINT.debuff]
    EFF_POWER = 3

    def y_cost(self, justCheck: bool, signal):
        enGrave = self.searchCards(LOCATION.grave, self.getEnemySideTuple(), CARD_TYPE.all, self)
        if not enGrave: return False
        if justCheck: return True
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck: return True
        enGrave = self.searchCards(LOCATION.grave, self.getEnemySideTuple(), CARD_TYPE.all, self)
        n = len(enGrave)
        if enGrave:
            yield self.y_banishCard(enGrave)
        if n > 0:
            yield self.y_damagePlayer(self.getEnemySideTuple(), n*200)
        return True
