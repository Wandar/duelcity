# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:upsword
卡名:升腾之剑
"""

#########################my

"""
1A:选择自己场上1只战士族怪兽,使其{ATK}+700直到回合结束
"""

class tupsword(Card):
    CARD_KEY="upsword"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tupsword_effect1)

class tupsword_effect1(Effect):
    effType = EFF_TYPE.active


    AI_HINT = [AI_HINT.addAtk]
    AI_POWER = 1

    def y_cost(self, justCheck:bool, signal):
        def f(c):
            return c.race == RACE.WARRIOR
        mons = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self, f)
        if not mons:
            return
        if justCheck:
            return True
        target = yield self.y_select1Card(mons, TITLE.target, canCancel=True)
        if target:
            self.saveTarget1(target)
            return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        target = self.getLegalTarget1()
        if target:
            yield self.y_addCardData(target, attackAdd=700, effDuration=EFF_DURATION.utilTurnEnds)
