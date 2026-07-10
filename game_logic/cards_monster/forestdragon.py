# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Vivid Green Dragon
卡名:苍翠龙
效果:1T:<召唤时>:随机发现2只等级3以下的植物族怪兽特殊召唤。2P:自己场上其他植物族怪兽{ATK}{DEF}+400。
"""

class forestdragon(Card):
    CARD_KEY = 'forestdragon'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(forestdragon_e1)
        self.initEffect(forestdragon_e2)


class forestdragon_e1(Effect):
    # 1T:<召唤时>:随机发现2只等级3以下的植物族怪兽特殊召唤。
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
        # 发现并特殊召唤至多2只等级3以下的植物族怪兽
        for _ in range(2):
            if self.freeMonsterSpace() <= 0:
                break
            picked = yield self.y_discoverCard(title=TITLE.specialSummon, side=self.getSide(), race=RACE.PLANT,
                                               cardType=CARD_TYPE.monster, maxLevel=3,
                                               count=3, canCancel=True)
            if not picked:
                break
            yield self.y_specialSummon(picked)
        return True


class forestdragon_e2(Effect):
    # 2P:自己场上其他植物族怪兽{ATK}{DEF}+400。
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
        def isOtherPlant(c):
            return c != self.owner and c.race == RACE.PLANT
        targets = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, None, isOtherPlant)
        if targets:
            yield self.y_addCardData(targets, attackAdd=400, defenceAdd=400,
                                     effDuration=EFF_DURATION.fromSource, uniqueSourceID=self.effUniID)
