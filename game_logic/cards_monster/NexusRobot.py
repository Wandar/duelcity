# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Nexus Robot
卡名:脉冲机器人
效果:1T:<召唤时>:从手牌把1只等级2以下的机械族怪兽特殊召唤。
"""

class NexusRobot(Card):
    CARD_KEY = 'NexusRobot'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(NexusRobot_e1)


class NexusRobot_e1(Effect):
    # 1T:<召唤时>:从手牌把1只等级2以下的机械族怪兽特殊召唤。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        def isTarget(c):
            return c.race == RACE.MACHINE and c.level <= 2
        targets = self.searchCards(LOCATION.hand, self.getSide(), CARD_TYPE.monster, self, isTarget)
        if not targets:
            return False
        if self.freeMonsterSpace() == 0:
            return False
        if justCheck:
            return True
        chosen = yield self.y_select1Card(targets, TITLE.specialSummon, canCancel=True)
        if not chosen:
            return False
        self.saveTarget1(chosen)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1()
        if not t:
            return False
        yield self.y_specialSummon(t)
        return True

