# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Quantum Scout Spider
卡名:量子侦察蛛
效果:1T:<召唤时>:把对方场上攻击力最高的1只怪兽变为守备表示且无法变更表示形式。
"""

class Sci_Fi_Robot_Spider_Prefab(Card):
    CARD_KEY = 'Sci-Fi_Robot_Spider Prefab'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Sci_Fi_Robot_Spider_Prefab_e1)


class Sci_Fi_Robot_Spider_Prefab_e1(Effect):
    # 1T:<召唤时>:把对方场上攻击力最高的1只怪兽变为守备表示且无法变更表示形式。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.debuff]
    EFF_POWER = 3

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
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        def isAtk(c):
            return c.isFaceUp() and c.form == FORM.attack
        enemies = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self, isAtk)
        if not enemies:
            return False
        maxAtk = max(c.atk for c in enemies)
        target = next(c for c in enemies if c.atk == maxAtk)
        yield self.y_changeForm(target, FORM.defence)
        return True
