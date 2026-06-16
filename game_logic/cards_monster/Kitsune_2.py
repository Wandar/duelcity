# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Raccoon Knight
卡名:浣熊骑士
效果:1A:[把1张手牌送入弃牌区]:把对方场上1只攻击力1000以下的怪兽变为守备表示。
"""

class Kitsune_2(Card):
    CARD_KEY = 'Kitsune_2'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Kitsune_2_e1)


class Kitsune_2_e1(Effect):
    # 1A:[把1张手牌送入弃牌区]:把对方场上1只攻击力1000以下的怪兽变为守备表示。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.debuff, AI_HINT.costHand]
    EFF_POWER = 2

    def y_cost(self, justCheck, signal):
        hand = self.searchCards(LOCATION.hand, self.getSide(), CARD_TYPE.all, self)
        if not hand:
            return False
        def isT(c):
            return c.isFaceUp() and c.form == FORM.attack and c.atk <= 1000
        enemies = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self, isT)
        if not enemies:
            return False
        if justCheck:
            return True
        cost = yield self.y_select1Card(hand, TITLE.sendToGrave, canCancel=True)
        if not cost:
            return False
        target = yield self.y_select1Card(enemies, TITLE.changeForm, canCancel=True)
        if not target:
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

