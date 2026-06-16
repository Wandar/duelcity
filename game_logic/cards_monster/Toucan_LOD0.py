# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Toucan
卡名:巨嘴鸟
效果:1T:<召唤时>:把1张手牌放回卡组底部,自己抽1张卡。
"""

class Toucan_LOD0(Card):
    CARD_KEY = 'Toucan_LOD0'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Toucan_LOD0_e1)


class Toucan_LOD0_e1(Effect):
    # 1T:<召唤时>:把1张手牌放回卡组底部,自己抽1张卡。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.drawCard]
    EFF_POWER = 1

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        hand = self.searchCards(LOCATION.hand, self.getSide(), CARD_TYPE.all, self)
        if not hand:
            return False
        if justCheck:
            return True
        chosen = yield self.y_select1Card(hand, TITLE.returnToDeck, canCancel=True)
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
        yield self.y_returnCardToDeck(t, self.getSide(), RETURN_TO_DECK.bottom)
        if len(self.game.decks[self.getSide()]) > 0:
            yield self.y_drawCard(self.getSide(), 1)
        return True

