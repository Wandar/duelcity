# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Polar Ice Dragon
卡名:极冰龙
效果:1P:<对方回合结束时>:选对方场上一只怪兽变为守备表示。
"""

class polardragon(Card):
    CARD_KEY = 'polardragon'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(polardragon_e1)


class polardragon_e1(Effect):
    # 1P:<对方回合结束时>:选对方场上一只怪兽变为守备表示。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.TurnEnds])
    AI_HINT = [AI_HINT.debuff]
    EFF_POWER = 2

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.TurnEnds):
            return False
        if self.game.whoseTurn == self.getSide():
            return False
        if not self.owner.isMonsterOnField():
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

