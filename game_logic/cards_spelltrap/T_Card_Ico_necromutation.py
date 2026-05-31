# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_necromutation
卡名:亡灵变异
"""

#########################my

"""
1A:[Cost:支付1500基本分]:自己场上1只怪兽变为不死族,并{ATK}+600
"""

class tT_Card_Ico_necromutation(Card):
    CARD_KEY="T_Card_Ico_necromutation"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_necromutation_effect1)

class tT_Card_Ico_necromutation_effect1(Effect):
    effType = EFF_TYPE.active


    AI_HINT = [AI_HINT.addAtk]
    AI_POWER = 1

    def y_cost(self, justCheck:bool, signal):
        if self.game.getPlayerLP(self.getSide()) <= 1500:
            return
        myMon = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self)
        if not myMon:
            return
        if justCheck:
            return True
        target = yield self.y_select1Card(myMon, TITLE.target, canCancel=True)
        if target:
            yield self.y_damagePlayer(self.getSide(), 1500)
            self.saveTarget1(target)
            return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        target = self.getLegalTarget1()
        if target:
            yield self.y_changeCardData(target, newRace=RACE.ZOMBIE)
            yield self.y_addCardData(target, attackAdd=600)
