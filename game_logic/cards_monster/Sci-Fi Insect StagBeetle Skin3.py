# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Mecha Stag Beetle
卡名:机械锹形虫
效果:1A:[把1只我方怪兽返回手牌]:发现一张等级4以下的机械族怪兽并特殊召唤。2T:<我方准备阶段>:此卡攻击力·守备力上升400。
"""

class Sci_Fi_Insect_StagBeetle_Skin3(Card):
    CARD_KEY = 'Sci-Fi Insect StagBeetle Skin3'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Sci_Fi_Insect_StagBeetle_Skin3_e1)
        self.initEffect(Sci_Fi_Insect_StagBeetle_Skin3_e2)


class Sci_Fi_Insect_StagBeetle_Skin3_e1(Effect):
    # 1A:[把1只我方怪兽返回手牌]:发现一张等级4以下的机械族怪兽并特殊召唤。
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
                                           cardType=CARD_TYPE.monster, maxLevel=4, count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked)
        return True


class Sci_Fi_Insect_StagBeetle_Skin3_e2(Effect):
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
