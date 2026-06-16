# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Giantclaw Drakebeast
卡名:巨爪龙兽
效果:1A:[把此卡解放]:破坏对方场上所有守备表示的怪兽。
"""

class Dragonrace(Card):
    CARD_KEY = 'Dragonrace'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Dragonrace_e1)


class Dragonrace_e1(Effect):
    # 1A:[把此卡解放]:破坏对方场上所有守备表示的怪兽。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 4

    def y_cost(self, justCheck, signal):
        def isDef(c):
            return c.form in (FORM.defence, FORM.defenceSet)
        targets = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self, isDef)
        if not targets:
            return False
        if justCheck:
            return True
        successNum = yield self.y_tributeCard(self.owner)
        if not successNum:
            return False
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        def isDef(c):
            return c.form in (FORM.defence, FORM.defenceSet)
        targets = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self, isDef)
        if targets:
            yield self.y_destroyCard(targets)
        return True

