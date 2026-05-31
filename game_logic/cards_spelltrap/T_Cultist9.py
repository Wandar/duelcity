# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Cultist9
卡名:邪教雷击
"""

#########################my

"""
1A:对对方造成500伤害,如果自己场上存在暗属性怪兽,改为800
"""

class tT_Cultist9(Card):
    CARD_KEY="T_Cultist9"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Cultist9_effect1)

class tT_Cultist9_effect1(Effect):
    effType = EFF_TYPE.active


    AI_HINT = [AI_HINT.eraser]
    AI_POWER = 1

    enemy = 0
    def y_cost(self, justCheck:bool, signal):
        if justCheck:
            return True
        self.enemy = yield self.y_select1EnemySide()
        return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        def f(c):
            return c.attr == ATTR.DARK
        darks = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self, f)
        dmg = 800 if darks else 500
        yield self.y_damagePlayer(self.enemy, dmg)
