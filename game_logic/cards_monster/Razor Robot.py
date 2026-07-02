# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Spikewheel Warbot
卡名:刺轮战机
效果:1T:<召唤时>:发现一张等级4以下的机械族怪兽并特殊召唤。2T:<我方准备阶段>:此卡攻击力·守备力上升400。
"""

class Razor_Robot(Card):
    CARD_KEY = "Razor Robot"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Razor_Robot_e1)
        self.initEffect(Razor_Robot_e2)


class Razor_Robot_e1(Effect):
    # 1T:<召唤时>:发现一张等级4以下的机械族怪兽并特殊召唤。
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
        picked = yield self.y_discoverCard(title=TITLE.specialSummon, side=self.getSide(), race=RACE.MACHINE,
                                           cardType=CARD_TYPE.monster, maxLevel=4, count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked)
        return True


class Razor_Robot_e2(Effect):
    # 2T:<我方准备阶段>:此卡攻击力·守备力上升400。
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
        yield self.y_addCardData(self.owner, attackAdd=400, defenceAdd=400, effDuration=EFF_DURATION.onceForever)
        return True
