# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Gleaming Steed Pegasus
卡名:光辉小马
效果:1T:<召唤时>:从自己弃牌区把1张魔法卡加入手牌。
"""

class cartoonPegasus(Card):
    CARD_KEY = 'cartoonPegasus'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(cartoonPegasus_e1)


class cartoonPegasus_e1(Effect):
    # 1T:<召唤时>:从自己弃牌区把1张魔法卡加入手牌。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.earn]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        spells = self.searchCards(LOCATION.grave, self.getSide(), CARD_TYPE.spell, self)
        if not spells:
            return False
        if self.game.freeSpellSpace(self.getSide()) == 0 and False:
            return False
        if justCheck:
            return True
        chosen = yield self.y_select1Card(spells, TITLE.addToHand, canCancel=True)
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

