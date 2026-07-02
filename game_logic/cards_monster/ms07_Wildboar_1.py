# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Flower-Crowned Piglet
卡名:花冠小猪
效果:1A:[支付800基本分]:发现一张等级2以下的兽族怪兽并沉默召唤。
"""

class ms07_Wildboar_1(Card):
    CARD_KEY = 'ms07_Wildboar_1'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(ms07_Wildboar_1_e1)


class ms07_Wildboar_1_e1(Effect):
    # 1A:[支付800基本分]:发现一张等级2以下的兽族怪兽并沉默召唤。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.summoner, AI_HINT.highCost]
    EFF_POWER = 4

    def y_cost(self, justCheck, signal):
        if self.game.LPs[self.getSide()] <= 800:
            return False
        if self.freeMonsterSpace() == 0:
            return False
        if justCheck:
            return True
        yield self.y_damagePlayer(self.getSide(), 800)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        if self.freeMonsterSpace() == 0:
            return False
        picked = yield self.y_discoverCard(title=TITLE.specialSummon, side=self.getSide(), race=RACE.BEAST,
                                           cardType=CARD_TYPE.monster, maxLevel=2, count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked)
            if picked.isMonsterOnField():
                yield self.y_silenceCard(picked, effDuration=EFF_DURATION.onceForever)
        return True
