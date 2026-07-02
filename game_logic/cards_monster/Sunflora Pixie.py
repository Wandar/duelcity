# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Sunlit Winged Sunflower King
卡名:向阳翼花王
效果:1T:<被破坏后>:发现一张等级4以下的植物族怪兽并特殊召唤。2A:[支付800基本分]:对对方造成600点伤害。
"""

class Sunflora_Pixie(Card):
    CARD_KEY = "Sunflora Pixie"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Sunflora_Pixie_e1)
        self.initEffect(Sunflora_Pixie_e2)


class Sunflora_Pixie_e1(Effect):
    # 1T:<被破坏后>:发现一张等级4以下的植物族怪兽并特殊召唤。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.grave, [Signal.Destroyed])
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 4

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Destroyed, self.owner):
            return False
        if self.freeMonsterSpace() == 0:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        picked = yield self.y_discoverCard(title=TITLE.specialSummon, side=self.getSide(), race=RACE.PLANT,
                                           cardType=CARD_TYPE.monster, maxLevel=4, count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked)
        return True


class Sunflora_Pixie_e2(Effect):
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
