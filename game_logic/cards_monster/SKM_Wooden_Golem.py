# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Wildwood Golem
卡名:荒野木傀儡
效果:1A:[把1张手牌送入弃牌区]:把对方场上1只怪兽变为守备表示且本回合无法变更表示形式。
"""

class SKM_Wooden_Golem(Card):
    CARD_KEY = 'SKM_Wooden_Golem'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(SKM_Wooden_Golem_e1)


class SKM_Wooden_Golem_e1(Effect):
    # 1A:[把1张手牌送入弃牌区]:把对方场上1只怪兽变为守备表示且本回合无法变更表示形式。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.debuff]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        hand = self.searchCards(LOCATION.hand, self.getSide(), CARD_TYPE.all, self)
        if not hand:
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
        cost = yield self.y_select1Card(hand, TITLE.discard, canCancel=True)
        if not cost:
            return False
        yield self.y_sendCardToGrave(cost)
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
