# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Scarlet-Maned Autumn Giant
卡名:红鬃秋巨人
"""

class Giant_Autumn(Card):
    CARD_KEY="Giant_Autumn"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(Giant_Autumn_e1)


"""
1T:自己回合结束时,从卡组把1张植物族怪兽送入弃牌区。
"""
class Giant_Autumn_e1(Effect):
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.TurnEnds])
    AI_HINT = [AI_HINT.enhance]
    EFF_POWER = 2

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.TurnEnds):
            return False
        if self.game.whoseTurn != self.getSide():
            return False

        def isTarget(card):
            return card.race == RACE.PLANT

        targets = self.searchCards(LOCATION.deck, self.getSide(), CARD_TYPE.monster, self, isTarget)
        if not targets:
            return False
        if justCheck:
            return True

        chosen = yield self.y_select1Card(targets, TITLE.sendToGrave)
        if not chosen:
            return False
        self.saveTarget1(chosen)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        target = self.getLegalTarget1(checkLocationChange=False)
        if not target:
            return False
        yield self.y_sendCardToGrave(target)
        return True
