# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Blastfire Hound
卡名:爆火狂犬
效果:1A:[丢弃1张手牌]:发现一张等级4以下的兽战士族怪兽并特殊召唤。2P:我方场上其他兽战士族怪兽攻击力·守备力上升400。
"""

class Dog_Bowwow(Card):
    CARD_KEY = "Dog Bowwow"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Dog_Bowwow_e1)
        self.initEffect(Dog_Bowwow_e2)


class Dog_Bowwow_e1(Effect):
    # 1A:[丢弃1张手牌]:发现一张等级4以下的兽战士族怪兽并特殊召唤。
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
        picked = yield self.y_discoverCard(title=TITLE.specialSummon, side=self.getSide(), race=RACE.BEASTWARRIOR,
                                           cardType=CARD_TYPE.monster, maxLevel=4, count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked)
        return True


class Dog_Bowwow_e2(Effect):
    # 2P:我方场上其他兽战士族怪兽攻击力·守备力上升400。
    effType = EFF_TYPE.permanent
    observeSignals = (LOCATION.monsterZone, [Signal.AttachMonsterZone, Signal.DetachMonsterZone, Signal.CardRaceChanged])
    AI_HINT = [AI_HINT.permanent, AI_HINT.enhance]
    EFF_POWER = 3

    def y_signal(self, signal):
        if isSignal(signal, Signal.DetachMonsterZone, self.owner):
            allCards = self.searchCards(LOCATION.mask_all, -1, CARD_TYPE.all, None)
            yield self.y_removeBuffEffectSource(allCards, self.effUniID)
            return
        if isSignal(signal, Signal.DetachMonsterZone):
            yield self.y_removeBuffEffectSource(signal.card, self.effUniID)
            return
        if not self.owner.isMonsterOnField():
            return
        def isOtherBW(c):
            return c != self.owner and c.race == RACE.BEASTWARRIOR
        targets = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, None, isOtherBW)
        if targets:
            yield self.y_addCardData(targets, attackAdd=400, defenceAdd=400,
                                     effDuration=EFF_DURATION.fromSource, uniqueSourceID=self.effUniID)
