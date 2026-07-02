# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Jumping Raccoon
卡名:跳跳浣熊
效果:1A:[把此卡解放]:发现一张等级4以下的兽族怪兽并特殊召唤。2A:[支付800基本分]:对对方造成600点伤害。
"""

class toon_Raccoon(Card):
    CARD_KEY = "toon_Raccoon"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(toon_Raccoon_e1)
        self.initEffect(toon_Raccoon_e2)


class toon_Raccoon_e1(Effect):
    # 1A:[把此卡解放]:发现一张等级4以下的兽族怪兽并特殊召唤。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.summoner, AI_HINT.costMonster]
    EFF_POWER = 4

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
        picked = yield self.y_discoverCard(title=TITLE.specialSummon, side=self.getSide(), race=RACE.BEAST,
                                           cardType=CARD_TYPE.monster, maxLevel=4, count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked)
        return True


class toon_Raccoon_e2(Effect):
    # 2A:[支付800基本分]:对对方造成600点伤害。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.damager, AI_HINT.highCost]
    EFF_POWER = 2

    def y_cost(self, justCheck, signal):
        if self.game.LPs[self.getSide()] <= 800:
            return False
        if justCheck:
            return True
        yield self.y_damagePlayer(self.getSide(), 800)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        yield self.y_damagePlayer(self.getEnemySideTuple(), 600)
        return True
