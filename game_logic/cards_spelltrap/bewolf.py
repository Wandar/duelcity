# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Wolf Transformation
卡名:人狼变身
effect:
效果:1A:[耗费一只战士族怪兽]:从手牌特殊召唤一只等级6以下的兽战士族怪兽,并且{ATK}+100
"""

class tbewolf(Card):
    CARD_KEY = "bewolf"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(tbewolf_effect1)


class tbewolf_effect1(Effect):
    # 1A:[耗费一只战士族怪兽]:从手牌特殊召唤一只等级6以下的兽战士族怪兽,并且{ATK}+100
    effType = EFF_TYPE.active
    AI_HINT = [AI_HINT.summoner]
    AI_POWER = 3

    def y_cost(self, justCheck, signal):
        warriors = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self,
                                    lambda c: c.race == RACE.WARRIOR)
        if not warriors:
            return False
        handTargets = self.searchCards(LOCATION.hand, self.getSide(), CARD_TYPE.monster, self,
                                       lambda c: c.race == RACE.BEASTWARRIOR and c.level <= 6
                                                 and c.canSpecialSummon())
        if not handTargets:
            return False
        if self.freeMonsterSpace() == 0:
            return False
        if justCheck:
            return True
        tribute = yield self.y_select1Card(warriors, TITLE.tribute, canCancel=True)
        if not tribute:
            return False
        summonTarget = yield self.y_select1Card(handTargets, TITLE.specialSummon, canCancel=True)
        if not summonTarget:
            return False
        yield self.y_tributeCard([tribute])
        self.saveTarget1(summonTarget)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        target = self.getLegalTarget1()
        if target:
            yield self.y_specialSummon(target)
            yield self.y_addCardData(target, attackAdd=100, effDuration=EFF_DURATION.onceForever)
        return True
