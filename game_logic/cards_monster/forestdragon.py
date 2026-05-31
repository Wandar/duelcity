# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Vivid Green Dragon
卡名:苍翠龙
"""

class forestdragon(Card):
    CARD_KEY = "forestdragon"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(forestdragon_VerdantBurst)



"""
1A:<召唤时>[从自己卡组上面把10张卡除外]:这张卡的{ATK}变成10000{UTIL}。
1OT:<When summoned>[Banish the top 10 cards of your Deck]: This card's ATK becomes 10000 until the end of the turn.
"""
class forestdragon_VerdantBurst(Effect):
    effType = EFF_TYPE.optionalTrigger

    observeSignals = (LOCATION.monsterZone, [Signal.Summon])

    AI_HINT = [AI_HINT.addAtk]
    EFF_POWER = 5

    def y_cost(self, justCheck: bool, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        if signal.card != self.owner:
            return False

        deckCards = self.searchCards(LOCATION.deck, self.getSide(), CARD_TYPE.all, None)
        if len(deckCards) < 10:
            return False

        if justCheck:
            return True

        topTen = deckCards[:10]
        for c in topTen:
            yield self.y_locationChange(c, LOCATION.removed)
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck:
            return True
        yield self.y_changeCardData(
            self.owner, newAtk=10000, effDuration=EFF_DURATION.utilTurnEnds,
        )
        return True
