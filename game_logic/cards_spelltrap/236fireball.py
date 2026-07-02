# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:236fireball
卡名:236fireball
"""
"""
1A:如果自己场上有炎属性怪兽,对场上一只怪兽造成300点伤害
"""
class t236fireball(Card):
    CARD_KEY="236fireball"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(t236fireball_effect1)

class t236fireball_effect1(Effect):
    effType = EFF_TYPE.active

    AI_HINT = [AI_HINT.eraser]
    AI_POWER = 1

    def y_cost(self, justCheck:bool, signal):
        fireMonsters = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self,
                                         lambda c: c.attr == ATTR.FIRE)
        if not fireMonsters:
            return False
        targets = self.searchCards(LOCATION.monsterZone, -1, CARD_TYPE.monster, self)
        if not targets:
            return False
        if justCheck:
            return True
        target = yield self.y_select1Card(targets, TITLE.target, canCancel=True)
        if target:
            self.saveTarget1(target)
            return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        target = self.getLegalTarget1()
        if target:
            yield self.y_addCardData(target, attackAdd=-300, defenceAdd=-300,
                                     effDuration=EFF_DURATION.utilTurnEnds)
        return True
