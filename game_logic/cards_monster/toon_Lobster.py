# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Pinchy Lobster
卡名:钳钳龙虾
"""

class toon_Lobster(Card):
    CARD_KEY="toon_Lobster"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(toon_Lobster_e1)


"""
1T:<召唤时>:选择对方场上2张卡,对方从中选1张破坏。
"""
class toon_Lobster_e1(Effect):
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        enemyCards = self.searchCards(LOCATION.mask_onField, self.getEnemySideTuple(),
                                      CARD_TYPE.all, self)
        if not enemyCards:
            return False
        if justCheck:
            return True
        maxNum = min(2, len(enemyCards))
        chosen = yield self.y_selectCards(enemyCards, TITLE.target, minNum=1, maxNum=maxNum)
        if not chosen:
            return False
        self.saveTarget1(chosen)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        cards = self._getLegalTargetList1(False)
        if not cards:
            return False
        # the opponent picks which of the selected cards to destroy
        enemySide = self.getEnemySideTuple()[0]
        picked = yield self.y_select1Card(cards, TITLE.destroy, side=enemySide)
        if not picked:
            picked = cards[0]
        yield self.y_destroyCard(picked)
        return True
