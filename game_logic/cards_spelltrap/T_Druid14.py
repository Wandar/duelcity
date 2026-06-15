# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Druid14  【魔法】
卡图:深绿放射背景,中央深棕枫叶,边缘绿色荧光液体流淌,自然与魔法交融。
效果(AOTIP):
1A:自然恩泽——自己回复「自己场上怪兽数量×300」基本分,并使自己场上怪兽{DEF}+200。
"""

class tT_Druid14(Card):
    CARD_KEY = "T_Druid14"
    AUTHOR = "Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Druid14_eff)

class tT_Druid14_eff(Effect):
    effType = EFF_TYPE.active
    activateLocation = LOCATION.spellTrapZone
    AI_HINT = [AI_HINT.recoverLP, AI_HINT.enhance]
    EFF_POWER = 2

    def y_cost(self, justCheck: bool, signal):
        myMons = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self)
        if not myMons: return False
        if justCheck: return True
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck: return True
        myMons = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self)
        cnt = len(myMons)
        if cnt > 0:
            yield self.y_healPlayer(self.getSide(), cnt*300)
            yield self.y_addCardData(myMons, defenceAdd=200)
        return True
