# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Grove Goliath
卡名:林间巨灵
效果:1T:<我方准备阶段>:发现一张等级3以下的植物族怪兽并守备召唤。
"""

class Ent(Card):
    CARD_KEY = 'Ent'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Ent_e1)


class Ent_e1(Effect):
    # 1T:<我方准备阶段>:发现一张等级3以下的植物族怪兽并守备召唤。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.StandbyPhase])
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 4
    countLimit = COUNT_LIMIT.unlimited

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.StandbyPhase):
            return False
        if self.game.whoseTurn != self.getSide():
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
        picked = yield self.y_discoverCard(side=self.getSide(), race=RACE.PLANT,
                                           cardType=CARD_TYPE.monster, maxLevel=3, count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked, form=FORM.defence)
        return True
