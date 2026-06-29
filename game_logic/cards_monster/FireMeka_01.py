# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Crimsonflame Mechabeast
卡名:赤焰机甲兽
效果:1A:[把1只其他怪兽解放]:把对方场上1只怪兽变为守备表示且本回合无法变更表示形式。
"""

class FireMeka_01(Card):
    CARD_KEY = 'FireMeka_01'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(FireMeka_01_e1)


class FireMeka_01_e1(Effect):
    # 1A:[把1只其他怪兽解放]:把对方场上1只怪兽变为守备表示且本回合无法变更表示形式。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.debuff]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        def isOther(c):
            return c != self.owner
        fodder = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self, isOther)
        if not fodder:
            return False
        def isFace(c):
            return c.isFaceUp()
        enemies = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self, isFace)
        if not enemies:
            return False
        if justCheck:
            return True
        target = yield self.y_select1Card(enemies, TITLE.changeForm, canCancel=True)
        if not target:
            return False
        c = yield self.y_select1Card(fodder, TITLE.tribute, canCancel=True)
        if not c:
            return False
        successNum = yield self.y_tributeCard(c)
        if not successNum:
            return False
        self.saveTarget1(target)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1()
        if not t:
            return False
        yield self.y_changeForm(t, FORM.defence)
        return True
