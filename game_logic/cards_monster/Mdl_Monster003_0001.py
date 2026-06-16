# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Thunderstorm Dragon
卡名:轰鸣雷暴龙
效果:1A:[把此卡以外自己场上怪兽全部解放]:破坏对方场上所有怪兽,每破坏1只对对方造成300点伤害。
"""

class Mdl_Monster003_0001(Card):
    CARD_KEY = 'Mdl_Monster003_0001'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Mdl_Monster003_0001_e1)


class Mdl_Monster003_0001_e1(Effect):
    # 1A:[把此卡以外自己场上怪兽全部解放]:破坏对方场上所有怪兽,每破坏1只对对方造成300点伤害。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.eraser, AI_HINT.highCost]
    EFF_POWER = 5

    def y_cost(self, justCheck, signal):
        def isOther(c):
            return c != self.owner
        fodder = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self, isOther)
        if not fodder:
            return False
        enemies = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self)
        if not enemies:
            return False
        if justCheck:
            return True
        yield self.y_tributeCard(fodder)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        enemies = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self)
        n = yield self.y_destroyCard(enemies)
        if n and n > 0:
            yield self.y_damagePlayer(self.getEnemySideTuple(), 300 * n)
        return True

