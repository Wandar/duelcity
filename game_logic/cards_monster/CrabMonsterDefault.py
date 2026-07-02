# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Tiny Crab
卡名:迷你螃蟹
效果:1T:<被战斗破坏后>:发现1只等级4以下的水族怪兽以守备表示特殊召唤。
"""

class CrabMonsterDefault(Card):
    CARD_KEY = 'CrabMonsterDefault'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(CrabMonsterDefault_e1)


class CrabMonsterDefault_e1(Effect):
    # 1T:<被战斗破坏后>:发现1只等级4以下的水族怪兽以守备表示特殊召唤。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.grave, [Signal.DestroyedByBattle])
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 2

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.DestroyedByBattle, self.owner):
            return False
        if self.freeMonsterSpace() == 0:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        picked = yield self.y_discoverCard(title=TITLE.specialSummon, side=self.getSide(), race=RACE.AQUA,
                                           cardType=CARD_TYPE.monster, maxLevel=4, count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked, form=FORM.defence)
        return True
