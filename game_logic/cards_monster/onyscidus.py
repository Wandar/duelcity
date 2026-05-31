# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Onyscidus
卡名:等足虫
"""

class onyscidus(Card):
    CARD_KEY = "onyscidus"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(onyscidus_HiveAwakening)



"""
1T:<被战斗破坏时>:可以支付800基本分从自己卡组把1只4星的念动力族怪兽特殊召唤。
1T:<When destroyed by battle>[Pay 800 LP]: Special Summon 1 Level 4 INSECT monster from your Deck.
"""
class onyscidus_HiveAwakening(Effect):
    effType = EFF_TYPE.trigger

    observeSignals = (LOCATION.grave, [Signal.DestroyedByBattle])

    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 3

    def y_cost(self, justCheck: bool, signal):
        if not isSignal(signal, Signal.DestroyedByBattle, self.owner):
            return False
        if self.getPlayerLP(self.getSide()) < 800:
            return False

        def isTarget(c):
            return c.race == RACE.INSECT and c.level == 4

        targets = self.searchCards(LOCATION.deck, self.getSide(), CARD_TYPE.monster, self, isTarget)
        if not targets:
            return False
        if self.freeMonsterSpace() == 0:
            return False

        if justCheck:
            return True

        chosen = yield self.y_select1Card(targets, TITLE.specialSummon, canCancel=True)
        if not chosen:
            return False

        yield self.y_damagePlayer(self.getSide(), 800)
        self.saveTarget1(chosen)
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck:
            return True
        target = self.getLegalTarget1(checkLocationChange=False)
        if not target:
            return False
        yield self.y_specialSummon(target)
        return True
