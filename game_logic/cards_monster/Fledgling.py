# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Fledgling Wings of Dawn
卡名:破晓之雏翼
效果:1T:<对方怪兽召唤时>:发现一张等级2以下的鸟兽族怪兽并特殊召唤。
"""

class Fledgling(Card):
    CARD_KEY = 'Fledgling'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Fledgling_e1)


class Fledgling_e1(Effect):
    # 1T:<对方怪兽召唤时>:发现一张等级2以下的鸟兽族怪兽并特殊召唤。
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
        picked = yield self.y_discoverCard(title=TITLE.specialSummon, side=self.getSide(), race=RACE.WINDBEAST,
                                           cardType=CARD_TYPE.monster, maxLevel=2, count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked)
        return True
