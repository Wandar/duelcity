# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T Rex
卡名:暴龙
效果:1A:[从自己弃牌区除外2只恐龙族怪兽]:破坏对方场上1只怪兽。
"""

class T_Rex(Card):
    CARD_KEY = 'T Rex'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(T_Rex_e1)


class T_Rex_e1(Effect):
    # 1A:[从自己弃牌区除外2只恐龙族怪兽]:破坏对方场上1只怪兽。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.eraser, AI_HINT.highCost]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        def isDino(c):
            return c.race == RACE.DINOSAUR
        graveDinos = self.searchCards(LOCATION.grave, self.getSide(), CARD_TYPE.monster, self, isDino)
        if len(graveDinos) < 2:
            return False
        enemies = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self)
        if not enemies:
            return False
        if justCheck:
            return True
        cost = yield self.y_selectCards(graveDinos, TITLE.banish, self.getSide(), 2, 2, None, True)
        if not cost or len(cost) < 2:
            return False
        target = yield self.y_select1Card(enemies, TITLE.destroy, canCancel=True)
        if not target:
            return False
        yield self.y_banishCard(list(cost))
        self.saveTarget1(target)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1()
        if not t:
            return False
        yield self.y_destroyCard(t)
        return True

