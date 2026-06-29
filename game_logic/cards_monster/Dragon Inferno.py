# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Inferno Imp
卡名:爆炎小恶龙
效果:1T:<我方准备阶段>:发现一张等级3以下的龙族怪兽并守备召唤。
"""

class Dragon_Inferno(Card):
    CARD_KEY = "Dragon Inferno"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Dragon_Inferno_e1)


class Dragon_Inferno_e1(Effect):
    # 1T:<我方准备阶段>:发现一张等级3以下的龙族怪兽并守备召唤。
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
        picked = yield self.y_discoverCard(side=self.getSide(), race=RACE.DRAGON,
                                           cardType=CARD_TYPE.monster, maxLevel=3, count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked, form=FORM.defence)
        return True
