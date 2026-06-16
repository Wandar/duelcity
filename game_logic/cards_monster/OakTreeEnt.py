# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Oak Tree
卡名:橡树
效果:1P:自己回合结束时,此卡{ATK}+300、{DEF}+300。2T:<被破坏后>:随机生成2只LV2以下的植物族怪兽特殊召唤。
"""

class OakTreeEnt(Card):
    CARD_KEY = 'OakTreeEnt'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(OakTreeEnt_e1)
        self.initEffect(OakTreeEnt_e2)


class OakTreeEnt_e1(Effect):
    # 1P:自己回合结束时,此卡{ATK}+300、{DEF}+300。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.TurnEnds])
    AI_HINT = [AI_HINT.addAtk]
    EFF_POWER = 2
    countLimit = COUNT_LIMIT.unlimited

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.TurnEnds):
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
        yield self.y_addCardData(self.owner, attackAdd=300, defenceAdd=300,
                                 effDuration=EFF_DURATION.onceForever)
        return True


class OakTreeEnt_e2(Effect):
    # 2T:<被破坏后>:随机生成2只LV2以下的植物族怪兽特殊召唤。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.grave, [Signal.Destroyed])
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 3

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
        from DiscoverPool import DiscoverPool
        keys = DiscoverPool.instance().get(race=RACE.PLANT, cardType=CARD_TYPE.monster,
                                           maxLevel=2, count=2)
        for k in (keys or []):
            if self.freeMonsterSpace() == 0:
                break
            c = self.game.createCard(k, self.getSide())
            if c:
                yield self.y_specialSummon(c)
        return True

