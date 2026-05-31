# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:shieldbroken
卡名:shieldbroken
"""
"""
1A:破坏对方场上一只守备表示的怪兽
"""
class tshieldbroken(Card):
    CARD_KEY="shieldbroken"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tshieldbroken_effect1)

class tshieldbroken_effect1(Effect):
    effType = EFF_TYPE.active

    AI_HINT = [AI_HINT.eraser]
    AI_POWER = 2

    def y_cost(self, justCheck:bool, signal):
        defMonsters = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(),
                                        CARD_TYPE.monster, self,
                                        lambda c: c.form == FORM.defense)
        if not defMonsters:
            return False
        if justCheck:
            return True
        target = yield self.y_select1Card(defMonsters, TITLE.destroy, canCancel=True)
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
