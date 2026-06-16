# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Moth
卡名:蛾
效果:1T:<召唤时>:从弃牌区把1只昆虫族怪兽返回手牌。
"""

class Moth(Card):
    CARD_KEY = 'Moth'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Moth_e1)


class Moth_e1(Effect):
    # 1T:<召唤时>:从弃牌区把1只昆虫族怪兽返回手牌。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.earn]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        def isInsect(c):
            return c.race == RACE.INSECT
        targets = self.searchCards(LOCATION.grave, self.getSide(), CARD_TYPE.monster, self, isInsect)
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

