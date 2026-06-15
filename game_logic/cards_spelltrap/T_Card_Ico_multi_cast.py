# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_multi_cast  【魔法】
卡图:紫粉放射背景,蓝色手掌托举橙色小动物,左右光圈包裹小怪兽,多重施法。
效果(AOTIP):
1A:多重施放——从自己手卡特殊召唤最多2只怪兽。
"""

class tT_Card_Ico_multi_cast(Card):
    CARD_KEY = "T_Card_Ico_multi_cast"
    AUTHOR = "Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_multi_cast_eff)

class tT_Card_Ico_multi_cast_eff(Effect):
    effType = EFF_TYPE.active
    activateLocation = LOCATION.spellTrapZone
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 3

    def y_cost(self, justCheck: bool, signal):
        handMons = self.searchCards(LOCATION.hand, self.getSide(), CARD_TYPE.monster, self)
        if not handMons or not self.freeMonsterSpace(): return False
        if justCheck: return True
        maxN = min(2, self.freeMonsterSpace(), len(handMons))
        chosen = yield self.y_selectCards(handMons, TITLE.specialSummon, self.getSide(), 1, maxN, canCancel=True)
        if not chosen: return False
        self.saveTarget1(chosen)
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck: return True
        targets = self.getLegalTarget1()
        if targets:
            yield self.y_specialSummon(targets, self.getSide())
        return True
