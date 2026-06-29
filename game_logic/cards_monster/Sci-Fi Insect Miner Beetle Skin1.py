# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Gyro Gear Grub
卡名:旋轮机虫
效果:1A:[支付800基本分]:发现一张等级3以下的机械族怪兽并守备召唤。
"""

class Sci_Fi_Insect_Miner_Beetle_Skin1(Card):
    CARD_KEY = 'Sci-Fi Insect Miner Beetle Skin1'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Sci_Fi_Insect_Miner_Beetle_Skin1_e1)


class Sci_Fi_Insect_Miner_Beetle_Skin1_e1(Effect):
    # 1A:[支付800基本分]:发现一张等级3以下的机械族怪兽并守备召唤。
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
        picked = yield self.y_discoverCard(side=self.getSide(), race=RACE.MACHINE,
                                           cardType=CARD_TYPE.monster, maxLevel=3, count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked, form=FORM.defence)
        return True
