# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Were Snake
卡名:蛇人
"""

class weresnake(Card):
    CARD_KEY = "weresnake"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(weresnake_SheddingRebirth)



"""
1I:<场上效果>:<送入墓地时>[丢弃一张手牌]:从卡组特殊召唤一只LV4以下的爬虫类怪兽
1I:<When sent to the Graveyard>[Discard 1 card]: Special Summon 1 Level 4 or lower REPTILE monster from your Deck.
"""
class weresnake_SheddingRebirth(Effect):
    effType = EFF_TYPE.instant

    observeSignals = (LOCATION.grave, [Signal.EnterGrave])

    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 3

    def y_cost(self, justCheck: bool, signal):
        if not isSignal(signal, Signal.EnterGrave, self.owner):
            return False
        if signal.card != self.owner:
            return False

        hand = self.searchCards(LOCATION.hand, self.getSide(), CARD_TYPE.all, self)
        if not hand:
            return False

        def isTarget(c):
            return c.race == RACE.REPTILE and c.level <= 4

        deckTargets = self.searchCards(LOCATION.deck, self.getSide(), CARD_TYPE.monster, self, isTarget)
        if not deckTargets:
            return False
        if self.freeMonsterSpace() == 0:
            return False

        if justCheck:
            return True

        chosenDiscard = yield self.y_select1Card(hand, TITLE.discard, canCancel=True)
        if not chosenDiscard:
            return False
        chosenSummon = yield self.y_select1Card(deckTargets, TITLE.specialSummon, canCancel=True)
        if not chosenSummon:
            return False

        yield self.y_locationChange(chosenDiscard, LOCATION.grave)
        self.saveTarget1(chosenSummon)
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck:
            return True
        target = self.getLegalTarget1(checkLocationChange=False)
        if not target:
            return False
        yield self.y_specialSummon(target)
        return True
