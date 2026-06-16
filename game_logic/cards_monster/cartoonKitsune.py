# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Fluffbell
卡名:绒绒金铃
效果:1T:<召唤时>:确认双方卡组顶端各3张卡,并各自以任意顺序放回。
"""

class cartoonKitsune(Card):
    CARD_KEY = 'cartoonKitsune'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(cartoonKitsune_e1)


class cartoonKitsune_e1(Effect):
    # 1T:<召唤时>:确认双方卡组顶端各3张卡,并各自以任意顺序放回。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.search]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        for side in (self.getSide(),) + tuple(self.getEnemySideTuple()):
            deck = self.game.decks[side]
            if len(deck) < 1:
                continue
            top = list(reversed(deck[-3:]))  # top-first
            ordered = yield self.y_selectCards(top, TITLE.target, self.getSide(),
                                               len(top), len(top), None, False, hasOrder=True)
            if ordered:
                # 把选定顺序写回卡组顶端(列表尾部为顶端)
                rest = deck[:-len(top)]
                self.game.decks[side] = rest + list(reversed(ordered))
        return True

