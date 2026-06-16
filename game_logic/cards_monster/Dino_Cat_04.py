# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Little Totoro
卡名:小龙猫
效果:1A:<手牌效果:自己场上没有怪兽时>:把此卡特殊召唤。
"""

class Dino_Cat_04(Card):
    CARD_KEY = 'Dino_Cat_04'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Dino_Cat_04_e1)


class Dino_Cat_04_e1(Effect):
    # 1A:<手牌效果:自己场上没有怪兽时>:把此卡特殊召唤。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.hand
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 2

    def y_cost(self, justCheck, signal):
        if self.owner.location != LOCATION.hand:
            return False
        mine = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, None)
        if mine:
            return False
        if self.freeMonsterSpace() == 0:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        yield self.y_specialSummon(self.owner)
        return True

