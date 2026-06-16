# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Quantum Scout Spider
卡名:量子侦察蛛
效果:1T:<召唤时>:确认对方卡组顶2张,把1张送入弃牌区,自己抽1张卡。
"""

class Sci_Fi_Robot_Spider_Prefab(Card):
    CARD_KEY = 'Sci-Fi_Robot_Spider Prefab'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Sci_Fi_Robot_Spider_Prefab_e1)


class Sci_Fi_Robot_Spider_Prefab_e1(Effect):
    # 1T:<召唤时>:确认对方卡组顶2张,把1张送入弃牌区,自己抽1张卡。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.eraser, AI_HINT.drawCard]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        enemy = self.getEnemySideTuple()[0]
        if len(self.game.decks[enemy]) < 1:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        enemy = self.getEnemySideTuple()[0]
        deck = self.game.decks[enemy]
        top = list(reversed(deck[-2:]))
        if top:
            chosen = yield self.y_select1Card(top, TITLE.sendToGrave, self.getSide(), canCancel=True)
            if not chosen:
                chosen = top[0]
            yield self.y_sendCardToGrave(chosen)
        if len(self.game.decks[self.getSide()]) > 0:
            yield self.y_drawCard(self.getSide(), 1)
        return True

