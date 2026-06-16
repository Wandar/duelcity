# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Tiny Red Dragon
卡名:小红龙
效果:1T:<召唤时>:对对方场上1只守备表示的怪兽造成500点伤害。
"""

class cartoonWyvern(Card):
    CARD_KEY = 'cartoonWyvern'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(cartoonWyvern_e1)


class cartoonWyvern_e1(Effect):
    # 1T:<召唤时>:对对方场上1只守备表示的怪兽造成500点伤害。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.damager]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        def isDef(c):
            return c.form in (FORM.defence, FORM.defenceSet)
        targets = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self, isDef)
        if not targets:
            return False
        if justCheck:
            return True
        t = yield self.y_select1Card(targets, TITLE.damage, canCancel=True)
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
        yield self.y_damageCard(t, 500)
        return True

