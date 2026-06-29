# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Three-tailed Snow Wolf
卡名:三尾雪狼
效果:1T:<召唤时>:把对方场上1只怪兽变为守备表示且本回合无法变更表示形式。
"""

class ThreeTailedWolf(Card):
    CARD_KEY = 'ThreeTailedWolf'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(ThreeTailedWolf_e1)


class ThreeTailedWolf_e1(Effect):
    # 1T:<召唤时>:把对方场上1只怪兽变为守备表示且本回合无法变更表示形式。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.debuff]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        def isFaceUp(c):
            return c.isFaceUp()
        enemies = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self, isFaceUp)
        if not enemies:
            return False
        if justCheck:
            return True
        chosen = yield self.y_select1Card(enemies, TITLE.changeForm, canCancel=False)
        if not chosen:
            return False
        self.saveTarget1(chosen)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1()
        if not t:
            return False
        # y_changeForm 改为守备表示,并自动锁定本回合无法变更表示形式
        yield self.y_changeForm(t, FORM.defence)
        return True
