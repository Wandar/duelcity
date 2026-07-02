# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Dreamy Sea Dragon
卡名:梦幻海龙
效果:1T:<被破坏后>:发现一张等级5以下的龙族怪兽并特殊召唤。2A:[把1只其他怪兽解放]:破坏对方场上1张卡。
"""

class LDSea_Toon(Card):
    CARD_KEY = 'LDSea Toon'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(LDSea_Toon_e1)
        self.initEffect(LDSea_Toon_e2)


class LDSea_Toon_e1(Effect):
    # 1T:<被破坏后>:发现一张等级5以下的龙族怪兽并特殊召唤。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.grave, [Signal.Destroyed])
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 4

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
        picked = yield self.y_discoverCard(title=TITLE.specialSummon, side=self.getSide(), race=RACE.DRAGON,
                                           cardType=CARD_TYPE.monster, maxLevel=5, count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked)
        return True


class LDSea_Toon_e2(Effect):
    # 2A:[把1只其他怪兽解放]:破坏对方场上1张卡。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.eraser, AI_HINT.costMonster]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        def isOther(c):
            return c != self.owner
        fodder = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self, isOther)
        if not fodder:
            return False
        enemyCards = self.searchCards(LOCATION.mask_onField, self.getEnemySideTuple(), CARD_TYPE.all, self)
        if not enemyCards:
            return False
        if justCheck:
            return True
        cost = yield self.y_select1Card(fodder, TITLE.tribute, canCancel=True)
        if not cost:
            return False
        target = yield self.y_select1Card(enemyCards, TITLE.destroy, canCancel=True)
        if not target:
            return False
        successNum = yield self.y_tributeCard(cost)
        if not successNum:
            return False
        self.saveTarget1(target)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1()
        if not t:
            return False
        yield self.y_destroyCard(t)
        return True
