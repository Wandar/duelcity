# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Predator Drakonoid
卡名:捕食机龙
效果:1A:[把自己场上1只其他机械族怪兽送入弃牌区]:把对方场上1只怪兽除外。
"""

class Dragon_Predator_Robot(Card):
    CARD_KEY = 'Dragon Predator Robot'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Dragon_Predator_Robot_e1)


class Dragon_Predator_Robot_e1(Effect):
    # 1A:[把自己场上1只其他机械族怪兽送入弃牌区]:把对方场上1只怪兽除外。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.eraser, AI_HINT.costMonster]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        def isFodder(c):
            return c != self.owner and c.race == RACE.MACHINE
        fodder = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self, isFodder)
        if not fodder:
            return False
        enemies = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self)
        if not enemies:
            return False
        if justCheck:
            return True
        cost = yield self.y_select1Card(fodder, TITLE.sendToGrave, canCancel=True)
        if not cost:
            return False
        target = yield self.y_select1Card(enemies, TITLE.banish, canCancel=True)
        if not target:
            return False
        yield self.y_sendCardToGrave(cost)
        self.saveTarget1(target)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1()
        if not t:
            return False
        yield self.y_banishCard(t)
        return True

