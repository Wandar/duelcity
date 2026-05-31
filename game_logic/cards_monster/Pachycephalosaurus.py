# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Pachycephalosaurus
卡名:肿头龙
"""

class Pachycephalosaurus(Card):
    CARD_KEY = "Pachycephalosaurus"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Pachycephalosaurus_HardHeadedLegacy)


"""
1T:<被效果破坏时>:从卡组把1只4星以下的恐龙族怪兽特殊召唤。
1T:<When destroyed by effect>:Special Summon 1 Level 4 or lower DINOSAUR monster from your Deck.
"""
class Pachycephalosaurus_HardHeadedLegacy(Effect):
    effType = EFF_TYPE.trigger

    observeSignals = (LOCATION.grave, [Signal.DestroyedByEffect])

    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 3

    def y_cost(self, justCheck: bool, signal):
        if not isSignal(signal, Signal.DestroyedByEffect, self.owner):
            return False

        def isTarget(card):
            return card.race == RACE.DINOSAUR and card.level <= 4

        targets = self.searchCards(
            LOCATION.deck, self.getSide(), CARD_TYPE.monster, self, isTarget
        )
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

    def y_activate(self, justCheck: bool, signal):
        if justCheck:
            return True

        target = self.getLegalTarget1(checkLocationChange=False)
        if not target:
            return False

        yield self.y_specialSummon(target)
        return True
