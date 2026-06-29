# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Predator Drakonoid
卡名:捕食机龙
效果:1A:[把1只我方怪兽返回手牌]:发现一张等级6以下的机械族怪兽并特殊召唤。2A:[把1只其他怪兽解放]:破坏对方场上1张卡。
"""

class Dragon_Predator_Robot(Card):
    CARD_KEY = "Dragon Predator Robot"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Dragon_Predator_Robot_e1)
        self.initEffect(Dragon_Predator_Robot_e2)


class Dragon_Predator_Robot_e1(Effect):
    # 1A:[把1只我方怪兽返回手牌]:发现一张等级6以下的机械族怪兽并特殊召唤。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.summoner, AI_HINT.costMonster]
    EFF_POWER = 4

    def y_cost(self, justCheck, signal):
        mine = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self)
        if not mine:
            return False
        if justCheck:
            return True
        cost = yield self.y_select1Card(mine, TITLE.returnToHand, canCancel=True)
        if not cost:
            return False
        yield self.y_returnCardToHand(cost)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        if self.freeMonsterSpace() == 0:
            return False
        picked = yield self.y_discoverCard(side=self.getSide(), race=RACE.MACHINE,
                                           cardType=CARD_TYPE.monster, maxLevel=6, count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked)
        return True


class Dragon_Predator_Robot_e2(Effect):
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
