# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Swirlthunder
卡名:漩漩雷云
效果:1T:<对方怪兽召唤时>:发现一张等级5以下的龙族怪兽并特殊召唤。2A:[支付800基本分]:对对方造成1000点伤害。
"""

class cartoonChineseDragon(Card):
    CARD_KEY = "cartoonChineseDragon"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(cartoonChineseDragon_e1)
        self.initEffect(cartoonChineseDragon_e2)


class cartoonChineseDragon_e1(Effect):
    # 1T:<对方怪兽召唤时>:发现一张等级5以下的龙族怪兽并特殊召唤。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 4

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon):
            return False
        scard = getattr(signal, "card", None)
        if scard is None or scard == self.owner or self.checkAlly(scard):
            return False
        if not self.owner.isMonsterOnField():
            return False
        if self.freeMonsterSpace() == 0:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        picked = yield self.y_discoverCard(side=self.getSide(), race=RACE.DRAGON,
                                           cardType=CARD_TYPE.monster, maxLevel=5, count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked)
        return True


class cartoonChineseDragon_e2(Effect):
    # 2A:[支付800基本分]:对对方造成1000点伤害。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.damager, AI_HINT.highCost]
    EFF_POWER = 3

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
        yield self.y_damagePlayer(self.getEnemySideTuple(), 1000)
        return True
