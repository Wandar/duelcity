# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Barbarian6
卡名:T_Barbarian6
"""
"""
1A:我方场上一只怪兽{ATK}{DEF}+400,然后破坏对方场上一张魔法陷阱卡
"""
class tT_Barbarian6(Card):
    CARD_KEY="T_Barbarian6"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Barbarian6_effect1)

class tT_Barbarian6_effect1(Effect):
    effType = EFF_TYPE.active

    AI_HINT = [AI_HINT.addAtk, AI_HINT.eraser]
    AI_POWER = 3

    def y_cost(self, justCheck:bool, signal):
        myMonsters = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self)
        if not myMonsters:
            return False
        enemySpells = self.searchCards(LOCATION.spellTrapZone, self.getEnemySideTuple(),
                                        CARD_TYPE.all, self)
        if justCheck:
            return True
        buffTarget = yield self.y_select1Card(myMonsters, TITLE.target, canCancel=True)
        if not buffTarget:
            return False
        self.saveTarget1(buffTarget)
        if enemySpells:
            destroyTarget = yield self.y_select1Card(enemySpells, TITLE.destroy, canCancel=True)
            if destroyTarget:
                self.saveTarget2(destroyTarget)
        return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        target = self.getLegalTarget1()
        if target:
            yield self.y_addCardData(target, attackAdd=400, defenceAdd=400,
                                     effDuration=EFF_DURATION.utilTurnEnds)
        target2 = self.getLegalTarget2()
        if target2:
            yield self.y_destroyCard(target2)
        return True
