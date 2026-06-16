# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Wings of Dawn
卡名:破晓之翼
效果:1P:自己的准备阶段,双方场上守备表示的怪兽全部变为攻击表示。
"""

class littleBird(Card):
    CARD_KEY = 'littleBird'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(littleBird_e1)


class littleBird_e1(Effect):
    # 1P:自己的准备阶段,双方场上守备表示的怪兽全部变为攻击表示。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.StandbyPhase])
    AI_HINT = [AI_HINT.battleBenefit]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.StandbyPhase):
            return False
        if self.game.whoseTurn != self.getSide():
            return False
        if not self.owner.isMonsterOnField():
            return False
        def isDef(c):
            return c.form in (FORM.defence, FORM.defenceSet)
        defs = self.searchCards(LOCATION.monsterZone, -1, CARD_TYPE.monster, None, isDef)
        if not defs:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        def isDef(c):
            return c.form in (FORM.defence, FORM.defenceSet)
        defs = self.searchCards(LOCATION.monsterZone, -1, CARD_TYPE.monster, None, isDef)
        if defs:
            yield self.y_changeForm(defs, FORM.attack)
        return True

