# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Spikedback Colossus Turtle
卡名:棘背巨龟
效果:1T:<召唤时>:发现一张等级4以下的水族怪兽并特殊召唤。2A:[丢弃1张手牌]:从卡组检索1只水族怪兽并覆盖。
"""

class Turtle_Blue_Shell_01(Card):
    CARD_KEY = 'Turtle_Blue_Shell_01'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Turtle_Blue_Shell_01_e1)
        self.initEffect(Turtle_Blue_Shell_01_e2)


class Turtle_Blue_Shell_01_e1(Effect):
    # 1T:<召唤时>:发现一张等级4以下的水族怪兽并特殊召唤。
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
        picked = yield self.y_discoverCard(title=TITLE.specialSummon, side=self.getSide(), race=RACE.AQUA,
                                           cardType=CARD_TYPE.monster, maxLevel=4, count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked)
        return True


class Turtle_Blue_Shell_01_e2(Effect):
    # 2A:[丢弃1张手牌]:从卡组检索1只水族怪兽并覆盖。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.summoner, AI_HINT.costHand]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        hand = self.searchCards(LOCATION.hand, self.getSide(), CARD_TYPE.all, self)
        if not hand:
            return False
        def isR(c):
            return c.race == RACE.AQUA
        targets = self.searchCards(LOCATION.deck, self.getSide(), CARD_TYPE.monster, self, isR)
        if not targets:
            return False
        if self.freeMonsterSpace() == 0:
            return False
        if justCheck:
            return True
        cost = yield self.y_select1Card(hand, TITLE.discard, canCancel=True)
        if not cost:
            return False
        chosen = yield self.y_select1Card(targets, TITLE.specialSummon, canCancel=True)
        if not chosen:
            return False
        yield self.y_sendCardToGrave(cost)
        self.saveTarget1(chosen)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1(checkLocationChange=False)
        if not t or self.freeMonsterSpace() == 0:
            return False
        yield self.y_specialSummon(t, form=FORM.defenceSet)
        return True
