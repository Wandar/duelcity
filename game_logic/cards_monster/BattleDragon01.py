# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Tri-Headed Dragon King
卡名:三首龙王
效果:1A:[把1只其他怪兽解放]:发现一张等级4以下的龙族怪兽并特殊召唤。2P:我方场上其他龙族怪兽攻击力·守备力上升400。
"""

class BattleDragon01(Card):
    CARD_KEY = 'BattleDragon01'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(BattleDragon01_e1)
        self.initEffect(BattleDragon01_e2)


class BattleDragon01_e1(Effect):
    # 1A:[把1只其他怪兽解放]:发现一张等级4以下的龙族怪兽并特殊召唤。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.summoner, AI_HINT.costMonster]
    EFF_POWER = 4

    def y_cost(self, justCheck, signal):
        def isOther(c):
            return c != self.owner
        fodder = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self, isOther)
        if not fodder:
            return False
        if justCheck:
            return True
        cost = yield self.y_select1Card(fodder, TITLE.tribute, canCancel=True)
        if not cost:
            return False
        successNum = yield self.y_tributeCard(cost)
        if not successNum:
            return False
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        if self.freeMonsterSpace() == 0:
            return False
        picked = yield self.y_discoverCard(side=self.getSide(), race=RACE.DRAGON,
                                           cardType=CARD_TYPE.monster, maxLevel=4, count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked)
        return True


class BattleDragon01_e2(Effect):
    # 2P:我方场上其他龙族怪兽攻击力·守备力上升400。
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
        def isT(c):
            return c != self.owner and c.race == RACE.DRAGON
        targets = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, None, isT)
        if targets:
            yield self.y_addCardData(targets, attackAdd=400, defenceAdd=400,
                                     effDuration=EFF_DURATION.fromSource, uniqueSourceID=self.effUniID)
