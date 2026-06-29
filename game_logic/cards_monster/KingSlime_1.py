# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Slime King
卡名:史莱姆国王
效果:1A:[把1只我方怪兽返回手牌]:把对方场上1只怪兽变为守备表示且本回合无法变更表示形式。
"""

class KingSlime_1(Card):
    CARD_KEY = 'KingSlime_1'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(KingSlime_1_e1)


class KingSlime_1_e1(Effect):
    # 1A:[把1只我方怪兽返回手牌]:把对方场上1只怪兽变为守备表示且本回合无法变更表示形式。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.debuff]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        mine = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self)
        if not mine:
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
        rc = yield self.y_select1Card(mine, TITLE.returnToHand, canCancel=True)
        if not rc:
            return False
        yield self.y_returnCardToHand(rc)
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
