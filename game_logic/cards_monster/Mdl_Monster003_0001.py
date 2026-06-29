# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Thunderstorm Dragon
卡名:轰鸣雷暴龙
效果:1A:[把1张手牌送入弃牌区]:发现一张等级6以下的龙族怪兽并特殊召唤。2T:<我方准备阶段>:此卡攻击力·守备力上升500。
"""

class Mdl_Monster003_0001(Card):
    CARD_KEY = 'Mdl_Monster003_0001'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Mdl_Monster003_0001_e1)
        self.initEffect(Mdl_Monster003_0001_e2)


class Mdl_Monster003_0001_e1(Effect):
    # 1A:[把1张手牌送入弃牌区]:发现一张等级6以下的龙族怪兽并特殊召唤。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.summoner, AI_HINT.costHand]
    EFF_POWER = 4

    def y_cost(self, justCheck, signal):
        hand = self.searchCards(LOCATION.hand, self.getSide(), CARD_TYPE.all, self)
        if not hand:
            return False
        if self.freeMonsterSpace() == 0:
            return False
        if justCheck:
            return True
        cost = yield self.y_select1Card(hand, TITLE.discard, canCancel=True)
        if not cost:
            return False
        yield self.y_sendCardToGrave(cost)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        if self.freeMonsterSpace() == 0:
            return False
        picked = yield self.y_discoverCard(side=self.getSide(), race=RACE.DRAGON,
                                           cardType=CARD_TYPE.monster, maxLevel=6, count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked)
        return True


class Mdl_Monster003_0001_e2(Effect):
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
