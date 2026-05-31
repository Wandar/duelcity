# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_ShapeShifter2
卡名:形态变化
"""

#########################my

"""
1A:自己场上1只怪兽变为指定同族,{ATK}/{DEF}互换直到回合结束
"""

class tT_ShapeShifter2(Card):
    CARD_KEY="T_ShapeShifter2"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_ShapeShifter2_effect1)

class tT_ShapeShifter2_effect1(Effect):
    effType = EFF_TYPE.active


    AI_HINT = [AI_HINT.addAtk]
    AI_POWER = 1

    def y_cost(self, justCheck:bool, signal):
        myMon = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self)
        if not myMon:
            return
        if justCheck:
            return True
        target = yield self.y_select1Card(myMon, TITLE.target, canCancel=True)
        if target:
            self.saveTarget1(target)
            return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        target = self.getLegalTarget1()
        if target:
            origAtk, origDef = target.atk, target.def_
            yield self.y_changeCardData(target, newAtk=origDef, newDefence=origAtk, effDuration=EFF_DURATION.utilTurnEnds)
