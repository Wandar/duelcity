# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Tiny Breeze Sprite
卡名:微风小精灵
效果:1T:<此卡被特殊召唤时>:发现一张等级2以下的天使族怪兽并守备召唤。
"""

class Whirlwind(Card):
    CARD_KEY = 'Whirlwind'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Whirlwind_e1)


class Whirlwind_e1(Effect):
    # 1T:<此卡被特殊召唤时>:发现一张等级2以下的天使族怪兽并守备召唤。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.SpecialSummon])
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.SpecialSummon, self.owner):
            return False
        if self.freeMonsterSpace() == 0:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        picked = yield self.y_discoverCard(side=self.getSide(), race=RACE.FAIRY,
                                           cardType=CARD_TYPE.monster, maxLevel=2, count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked, form=FORM.defence)
        return True
