# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Armored Stone Golem
卡名:重甲石傀儡
效果:1A:[支付800基本分]:把对方场上1只怪兽变为守备表示且本回合无法变更表示形式。
"""

class SKM_Iron_Golem(Card):
    CARD_KEY = 'SKM_Iron_Golem'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(SKM_Iron_Golem_e1)


class SKM_Iron_Golem_e1(Effect):
    # 1A:[支付800基本分]:把对方场上1只怪兽变为守备表示且本回合无法变更表示形式。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.debuff]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if self.game.LPs[self.getSide()] <= 800:
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
        yield self.y_damagePlayer(self.getSide(), 800)
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
