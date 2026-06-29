# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Cloudhoof
卡名:云云麟角
效果:1T:<召唤时>:发现一张等级5以下的兽族怪兽并特殊召唤。2T:<我方准备阶段>:此卡攻击力·守备力上升600。
"""

class cartoonKirin(Card):
    CARD_KEY = "cartoonKirin"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(cartoonKirin_e1)
        self.initEffect(cartoonKirin_e2)


class cartoonKirin_e1(Effect):
    # 1T:<召唤时>:发现一张等级5以下的兽族怪兽并特殊召唤。
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
        picked = yield self.y_discoverCard(side=self.getSide(), race=RACE.BEAST,
                                           cardType=CARD_TYPE.monster, maxLevel=5, count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked)
        return True


class cartoonKirin_e2(Effect):
    # 2T:<我方准备阶段>:此卡攻击力·守备力上升600。
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
        yield self.y_addCardData(self.owner, attackAdd=600, defenceAdd=600, effDuration=EFF_DURATION.onceForever)
        return True
