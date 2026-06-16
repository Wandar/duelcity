# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Lyme
卡名:莱姆
效果:1A:[把此卡解放]:自己抽2张卡。
"""

class Lyme(Card):
    CARD_KEY = 'Lyme'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Lyme_e1)


class Lyme_e1(Effect):
    # 1A:[把此卡解放]:自己抽2张卡。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.drawCard]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if len(self.game.decks[self.getSide()]) < 1:
            return False
        if justCheck:
            return True
        successNum = yield self.y_tributeCard(self.owner)
        if not successNum:
            return False
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        n = min(2, len(self.game.decks[self.getSide()]))
        if n > 0:
            yield self.y_drawCard(self.getSide(), n)
        return True

