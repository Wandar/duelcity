# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Lava Scarlet Dragon
卡名:熔岩绯龙
效果:1T:<召唤时>:发现一张等级4以下的龙族怪兽并特殊召唤。2T:<我方准备阶段>:此卡攻击力·守备力上升500。
"""

class Dragon_Rd(Card):
    CARD_KEY = 'Dragon_Rd'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Dragon_Rd_e1)
        self.initEffect(Dragon_Rd_e2)


class Dragon_Rd_e1(Effect):
    # 1T:<召唤时>:发现一张等级4以下的龙族怪兽并特殊召唤。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 4

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
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
                                           cardType=CARD_TYPE.monster, maxLevel=4, count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked)
        return True


class Dragon_Rd_e2(Effect):
    # 2T:<我方准备阶段>:此卡攻击力·守备力上升500。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.StandbyPhase])
    AI_HINT = [AI_HINT.enhance]
    EFF_POWER = 2
    countLimit = COUNT_LIMIT.unlimited

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.StandbyPhase):
            return False
        if self.game.whoseTurn != self.getSide():
            return False
        if not self.owner.isMonsterOnField():
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        yield self.y_addCardData(self.owner, attackAdd=500, defenceAdd=500, effDuration=EFF_DURATION.onceForever)
        return True
