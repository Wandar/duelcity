# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_barrage
卡名:群体弹幕
"""

#########################my

"""
1A:自己场上每有1只怪兽,对对方造成200伤害
"""

class tT_Card_Ico_barrage(Card):
    CARD_KEY="T_Card_Ico_barrage"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_barrage_effect1)

class tT_Card_Ico_barrage_effect1(Effect):
    effType = EFF_TYPE.active


    AI_HINT = [AI_HINT.eraser]
    AI_POWER = 1

    enemy = 0
    def y_cost(self, justCheck:bool, signal):
        myMon = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self)
        if not myMon:
            return
        if justCheck:
            return True
        self.enemy = yield self.y_select1EnemySide()
        return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        myMon = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self)
        n = len(myMon)
        if n > 0:
            yield self.y_damagePlayer(self.enemy, 200 * n)
