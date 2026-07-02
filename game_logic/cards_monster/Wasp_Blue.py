# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Kingspike Wasp
卡名:毒刺蜂王
效果:1T:<被破坏后>:发现一张等级3以下的昆虫族怪兽并守备召唤。
"""

class Wasp_Blue(Card):
    CARD_KEY = 'Wasp_Blue'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Wasp_Blue_e1)


class Wasp_Blue_e1(Effect):
    # 1T:<被破坏后>:发现一张等级3以下的昆虫族怪兽并守备召唤。
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
        picked = yield self.y_discoverCard(title=TITLE.specialSummon, side=self.getSide(), race=RACE.INSECT,
                                           cardType=CARD_TYPE.monster, maxLevel=3, count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked, form=FORM.defence)
        return True
