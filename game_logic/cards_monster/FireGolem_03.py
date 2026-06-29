# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Marsh Mud Giant
卡名:沼泽泥巨人
效果:1A:[丢弃1张手牌]:把对方场上1只怪兽变为守备表示且本回合无法变更表示形式。
"""

class FireGolem_03(Card):
    CARD_KEY = 'FireGolem_03'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(FireGolem_03_e1)


class FireGolem_03_e1(Effect):
    # 1A:[丢弃1张手牌]:把对方场上1只怪兽变为守备表示且本回合无法变更表示形式。
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
