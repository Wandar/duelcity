# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_charge_battery
卡名:电池充能
"""

#########################my

"""
1A:选择自己场上1只雷族怪兽,使其{ATK}+800直到回合结束
"""

class tT_Card_Ico_charge_battery(Card):
    CARD_KEY="T_Card_Ico_charge_battery"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_charge_battery_effect1)

class tT_Card_Ico_charge_battery_effect1(Effect):
    effType = EFF_TYPE.active


    AI_HINT = [AI_HINT.addAtk]
    AI_POWER = 1

    def y_cost(self, justCheck:bool, signal):
        def f(c):
            return c.race == RACE.THUNDER
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
            yield self.y_addCardData(target, attackAdd=800, effDuration=EFF_DURATION.utilTurnEnds)
