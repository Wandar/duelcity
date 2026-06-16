# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Sweet Dream Gecko
卡名:甜梦幻蜥
效果:1T:<召唤时>:把对方场上1只怪兽变为守备表示。
"""

class EnemyCreature_V1(Card):
    CARD_KEY = 'EnemyCreature_V1'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(EnemyCreature_V1_e1)


class EnemyCreature_V1_e1(Effect):
    # 1T:<召唤时>:把对方场上1只怪兽变为守备表示。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.debuff]
    EFF_POWER = 2

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        def isAtk(c):
            return c.isFaceUp() and c.form == FORM.attack
        enemies = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self, isAtk)
        if not enemies:
            return False
        if justCheck:
            return True
        t = yield self.y_select1Card(enemies, TITLE.changeForm, canCancel=True)
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
        yield self.y_changeForm(t, FORM.defence)
        return True

