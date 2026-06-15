# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_barrage  【魔法】
卡图:橙红渐变,散落多只小动物以连发弹幕四散冲出。
效果(AOTIP):
1A:弹幕齐射——对对方造成「自己场上怪兽数量×300」的伤害。
"""

class tT_Card_Ico_barrage(Card):
    CARD_KEY = "T_Card_Ico_barrage"
    AUTHOR = "Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_barrage_eff)

class tT_Card_Ico_barrage_eff(Effect):
    effType = EFF_TYPE.active
    activateLocation = LOCATION.spellTrapZone
    AI_HINT = [AI_HINT.damager]
    EFF_POWER = 2

    def y_cost(self, justCheck: bool, signal):
        myMons = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self)
        if not myMons: return False
        if justCheck: return True
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck: return True
        cnt = len(self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self))
        if cnt > 0:
            yield self.y_damagePlayer(self.getEnemySideTuple(), cnt*300)
        return True
