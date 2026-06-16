# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Shadow Tiger
卡名:暗影虎
效果:1A:<墓地效果:自己的主要阶段>[把自己场上1只兽族怪兽送入弃牌区]:把此卡特殊召唤。
"""

class Tiger_Black(Card):
    CARD_KEY = 'Tiger_Black'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Tiger_Black_e1)


class Tiger_Black_e1(Effect):
    # 1A:<墓地效果:自己的主要阶段>[把自己场上1只兽族怪兽送入弃牌区]:把此卡特殊召唤。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.grave
    AI_HINT = [AI_HINT.summoner, AI_HINT.costMonster]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if self.owner.location != LOCATION.grave:
            return False
        if not self.game.isMainPhase():
            return False
        def isBeast(c):
            return c.race == RACE.BEAST
        fodder = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self, isBeast)
        if not fodder:
            return False
        if self.freeMonsterSpace() == 0:
            return False
        if justCheck:
            return True
        cost = yield self.y_select1Card(fodder, TITLE.sendToGrave, canCancel=True)
        if not cost:
            return False
        yield self.y_sendCardToGrave(cost)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        if self.freeMonsterSpace() == 0:
            return False
        yield self.y_specialSummon(self.owner)
        return True

