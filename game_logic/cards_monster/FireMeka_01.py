# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Crimsonflame Mechabeast
卡名:赤焰机甲兽
效果:1A:[把1张手牌送入弃牌区]:破坏对方场上1只攻击表示怪兽。
"""

class FireMeka_01(Card):
    CARD_KEY = 'FireMeka_01'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(FireMeka_01_e1)


class FireMeka_01_e1(Effect):
    # 1A:[把1张手牌送入弃牌区]:破坏对方场上1只攻击表示怪兽。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.eraser, AI_HINT.costHand]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        hand = self.searchCards(LOCATION.hand, self.getSide(), CARD_TYPE.all, self)
        if not hand:
            return False
        def isAtk(c):
            return c.isFaceUp() and c.form == FORM.attack
        enemies = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self, isAtk)
        if not enemies:
            return False
        if justCheck:
            return True
        cost = yield self.y_select1Card(hand, TITLE.sendToGrave, canCancel=True)
        if not cost:
            return False
        t = yield self.y_select1Card(enemies, TITLE.destroy, canCancel=True)
        if not t:
            return False
        yield self.y_sendCardToGrave(cost)
        self.saveTarget1(t)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1()
        if not t:
            return False
        yield self.y_destroyCard(t)
        return True

