# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_purge
卡名:净化清除
"""

#########################my

"""
1A:[自己场上全部魔法·陷阱卡送去墓地]:每张对对手造成200伤害
"""

class tT_Card_Ico_purge(Card):
    CARD_KEY="T_Card_Ico_purge"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_purge_effect1)

class tT_Card_Ico_purge_effect1(Effect):
    effType = EFF_TYPE.active


    AI_HINT = [AI_HINT.eraser]
    AI_POWER = 1

    enemy = 0
    def y_cost(self, justCheck:bool, signal):
        mySpells = self.searchCards(LOCATION.spellTrapZone, self.getSide(), CARD_TYPE.spell | CARD_TYPE.trap, self,
                                      lambda c: c is not self.owner)
        if not mySpells:
            return
        if justCheck:
            return True
        self.enemy = yield self.y_select1EnemySide()
        return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        mySpells = self.searchCards(LOCATION.spellTrapZone, self.getSide(), CARD_TYPE.spell | CARD_TYPE.trap, self,
                                     lambda c: c is not self.owner)
        n = len(mySpells)
        for c in mySpells:
            yield self.y_sendCardToGrave(c)
        if n:
            yield self.y_damagePlayer(self.enemy, 200 * n)
