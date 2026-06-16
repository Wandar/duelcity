# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Rhinoceros Beetle
卡名:独角仙
效果:1A:破坏对方场上1只守备表示的怪兽,此回合此卡不能攻击。
"""

class RhinocerosBeetle(Card):
    CARD_KEY = 'RhinocerosBeetle'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(RhinocerosBeetle_e1)


class RhinocerosBeetle_e1(Effect):
    # 1A:破坏对方场上1只守备表示的怪兽,此回合此卡不能攻击。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        def isDef(c):
            return c.form in (FORM.defence, FORM.defenceSet)
        targets = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self, isDef)
        if not targets:
            return False
        if justCheck:
            return True
        t = yield self.y_select1Card(targets, TITLE.destroy, canCancel=True)
        if not t:
            return False
        self.saveTarget1(t)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1()
        if not t:
            return False
        yield self.y_destroyCard(t)
        if self.owner.isMonsterOnField():
            yield self.y_changeCardData(self.owner, newAttackTimes=0, effDuration=EFF_DURATION.utilTurnEnds)
        return True

