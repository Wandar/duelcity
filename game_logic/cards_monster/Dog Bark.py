# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Blastfire Whelp Hound
卡名:爆火狂犬仔
效果:1T:<被战斗破坏后>:从手牌·卡组把1只「爆火狂犬」特殊召唤。
"""

class Dog_Bark(Card):
    CARD_KEY = 'Dog Bark'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Dog_Bark_e1)


class Dog_Bark_e1(Effect):
    # 1T:<被战斗破坏后>:从手牌·卡组把1只「爆火狂犬」特殊召唤。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.grave, [Signal.DestroyedByBattle])
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.DestroyedByBattle, self.owner):
            return False
        def isTarget(c):
            return c.cardKey == "Dog Bowwow"
        targets = self.searchCards(LOCATION.hand | LOCATION.deck, self.getSide(), CARD_TYPE.monster, self, isTarget)
        if not targets:
            return False
        if self.freeMonsterSpace() == 0:
            return False
        if justCheck:
            return True
        chosen = yield self.y_select1Card(targets, TITLE.specialSummon, canCancel=True)
        if not chosen:
            return False
        self.saveTarget1(chosen)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1(checkLocationChange=False)
        if not t:
            return False
        yield self.y_specialSummon(t)
        return True

