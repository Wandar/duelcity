# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Tiny Purple Dragon
卡名:小紫龙
效果:1A:[把此卡解放]:发现一张等级2以下的龙族怪兽并守备召唤。
"""

class cartoonDragon(Card):
    CARD_KEY = "cartoonDragon"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(cartoonDragon_e1)


class cartoonDragon_e1(Effect):
    # 1A:[把此卡解放]:发现一张等级2以下的龙族怪兽并守备召唤。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.summoner, AI_HINT.costMonster]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not self.owner.isMonsterOnField():
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
        if self.freeMonsterSpace() == 0:
            return False
        picked = yield self.y_discoverCard(side=self.getSide(), race=RACE.DRAGON,
                                           cardType=CARD_TYPE.monster, maxLevel=2, count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked, form=FORM.defence)
        return True
