# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Crimsonscale Dragon Knight
卡名:赤鳞龙骑士
效果:1T:<此卡被特殊召唤时>:把对方场上1只怪兽变为守备表示且本回合无法变更表示形式。
"""

class Dragonknight(Card):
    CARD_KEY = 'Dragonknight'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Dragonknight_e1)


class Dragonknight_e1(Effect):
    # 1T:<此卡被特殊召唤时>:把对方场上1只怪兽变为守备表示且本回合无法变更表示形式。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.SpecialSummon])
    AI_HINT = [AI_HINT.debuff]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.SpecialSummon, self.owner):
            return False
        def isAtk(c):
            return c.isFaceUp() and c.form == FORM.attack
        enemies = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self, isAtk)
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
        target = self.getLegalTarget1()
        if not target:
            return False
        yield self.y_changeForm(target, FORM.defence)
        return True
