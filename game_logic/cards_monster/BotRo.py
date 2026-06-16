# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:BotRo
卡名:飞行机械
效果:1T:<召唤时>:从卡组检索1只LV2的机械族怪兽。
"""

class BotRo(Card):
    CARD_KEY = 'BotRo'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(BotRo_e1)


class BotRo_e1(Effect):
    # 1T:<召唤时>:从卡组检索1只LV2的机械族怪兽。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.searchMonster]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        def isTarget(c):
            return c.race == RACE.MACHINE and c.level == 2
        targets = self.searchCards(LOCATION.deck, self.getSide(), CARD_TYPE.monster, self, isTarget)
        if not targets:
            return False
        if justCheck:
            return True
        chosen = yield self.y_select1Card(targets, TITLE.addToHand, canCancel=True)
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
        yield self.y_returnCardToHand(t)
        return True

