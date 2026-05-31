# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_
卡名:T_Card_Ico_
"""
"""
1A:我方场上一只怪兽{ATK}{DEF}+400,然后对对方场上一只怪兽造成400点伤害
"""
class tT_Card_Ico_(Card):
    CARD_KEY="T_Card_Ico_"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico__effect1)

class tT_Card_Ico__effect1(Effect):
    effType = EFF_TYPE.active

    AI_HINT = [AI_HINT.addAtk, AI_HINT.eraser]
    AI_POWER = 3

    def y_cost(self, justCheck:bool, signal):
        myMonsters = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self)
        enemyMonsters = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(),
                                          CARD_TYPE.monster, self)
        if not myMonsters or not enemyMonsters:
            return False
        if justCheck:
            return True
        buffT = yield self.y_select1Card(myMonsters, TITLE.target, canCancel=True)
        dmgT  = yield self.y_select1Card(enemyMonsters, TITLE.target, canCancel=True)
        if buffT and dmgT:
            self.saveTarget1(buffT)
            self.saveTarget2(dmgT)
            return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        buffT = self.getLegalTarget1()
        if buffT:
            yield self.y_addCardData(buffT, atkAdd=400, defAdd=400,
                                     effDuration=EFF_DURATION.utilTurnEnds)
        dmgT = self.getLegalTarget2()
        if dmgT:
            yield self.y_addCardData(dmgT, atkAdd=-400, defAdd=-400,
                                     effDuration=EFF_DURATION.utilTurnEnds)
        return True
