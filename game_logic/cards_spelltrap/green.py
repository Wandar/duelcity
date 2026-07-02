# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:green
卡名:green
"""
"""
1A:选择自己场上一只怪兽,使其种族变为植物族,{ATK}{DEF}+300
"""
class tgreen(Card):
    CARD_KEY="green"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tgreen_effect1)

class tgreen_effect1(Effect):
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
            target.setData("raceOverride", str(RACE.PLANT))
            yield self.y_addCardData(target, attackAdd=300, defenceAdd=300,
                                     effDuration=EFF_DURATION.utilTurnEnds)
        return True
