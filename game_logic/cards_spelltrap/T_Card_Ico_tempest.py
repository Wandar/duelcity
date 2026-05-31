# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_tempest
卡名:暴风雨
"""

#########################my

"""
1A:破坏场上所有魔法·陷阱卡,每破坏1张对对方造成200伤害
"""

class tT_Card_Ico_tempest(Card):
    CARD_KEY="T_Card_Ico_tempest"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_tempest_effect1)

class tT_Card_Ico_tempest_effect1(Effect):
    effType = EFF_TYPE.active


    AI_HINT = [AI_HINT.eraser]
    AI_POWER = 1

    enemy = 0
    def y_cost(self, justCheck:bool, signal):
        allST = self.searchCards(LOCATION.spellTrapZone, -1, CARD_TYPE.spell | CARD_TYPE.trap, self)
        if self.owner in allST:
            allST.remove(self.owner)
        if not allST:
            return
        if justCheck:
            return True
        self.enemy = yield self.y_select1EnemySide()
        return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        allST = self.searchCards(LOCATION.spellTrapZone, -1, CARD_TYPE.spell | CARD_TYPE.trap, self)
        if self.owner in allST:
            allST.remove(self.owner)
        destroyed = 0
        for c in allST:
            n = yield self.y_destroyCard(c)
            if n:
                destroyed += 1
        if destroyed:
            yield self.y_damagePlayer(self.enemy, 200 * destroyed)
