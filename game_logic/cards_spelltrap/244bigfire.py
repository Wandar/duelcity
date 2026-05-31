# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:244bigfire
卡名:244bigfire
"""
"""
1A:如果自己场上有炎属性怪兽,对对方场上一张魔法陷阱卡造成600点伤害
"""
class t244bigfire(Card):
    CARD_KEY="244bigfire"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(t244bigfire_effect1)

class t244bigfire_effect1(Effect):
    effType = EFF_TYPE.active

    AI_HINT = [AI_HINT.eraser]
    AI_POWER = 2

    def y_cost(self, justCheck:bool, signal):
        fireMonsters = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self,
                                         lambda c: c.attr == ATTR.FIRE)
        if not fireMonsters:
            return False
        enemySpells = self.searchCards(LOCATION.spellTrapZone, self.getEnemySideTuple(),
                                        CARD_TYPE.all, self)
        if not enemySpells:
            return False
        if justCheck:
            return True
        target = yield self.y_select1Card(enemySpells, TITLE.destroy, canCancel=True)
        if target:
            self.saveTarget1(target)
            return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        target = self.getLegalTarget1()
        if target:
            yield self.y_destroyCard(target)
        return True
