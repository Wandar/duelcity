# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:handgreen
卡名:handgreen
"""
"""
1A:选择自己场上一只怪兽,{ATK}{DEF}+200
"""
class thandgreen(Card):
    CARD_KEY="handgreen"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(thandgreen_effect1)

class thandgreen_effect1(Effect):
    effType = EFF_TYPE.active

    AI_HINT = [AI_HINT.addAtk]
    AI_POWER = 1

    def y_cost(self, justCheck:bool, signal):
        myMonsters = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self)
        if not myMonsters:
            return False
        if justCheck:
            return True
        target = yield self.y_select1Card(myMonsters, TITLE.target, canCancel=True)
        if target:
            self.saveTarget1(target)
            return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        target = self.getLegalTarget1()
        if target:
            yield self.y_addCardData(target, attackAdd=200, defenceAdd=200,
                                     effDuration=EFF_DURATION.utilTurnEnds)
        return True
