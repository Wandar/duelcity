# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Ptooey Llama
卡名:呸呸羊驼
效果:1T:<召唤时>:把对方场上1只怪兽返回持有者手牌,然后对方抽1张卡。
"""

class Llama_LOD0(Card):
    CARD_KEY = 'Llama_LOD0'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Llama_LOD0_e1)


class Llama_LOD0_e1(Effect):
    # 1T:<召唤时>:把对方场上1只怪兽返回持有者手牌,然后对方抽1张卡。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        enemies = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self)
        if not enemies:
            return False
        if justCheck:
            return True
        t = yield self.y_select1Card(enemies, TITLE.returnToHand, canCancel=True)
        if not t:
            return False
        self.saveTarget1(t)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1()
        if not t:
            return False
        enemySide = t.side
        yield self.y_returnCardToHand(t)
        if len(self.game.decks[enemySide]) > 0:
            yield self.y_drawCard(enemySide, 1)
        return True

