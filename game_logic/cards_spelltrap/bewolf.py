# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:bewolf
卡名:bewolf
"""
"""
1A:[Cost:献祭一只战士族怪兽]:从手牌特殊召唤一只LV6以下的兽战士族怪兽,并且{ATK}+400
"""
class tbewolf(Card):
    CARD_KEY="bewolf"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tbewolf_effect1)

class tbewolf_effect1(Effect):
    effType = EFF_TYPE.active

    AI_HINT = [AI_HINT.summoner]
    AI_POWER = 3

    def y_cost(self, justCheck:bool, signal):
        warriors = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self,
                                     lambda c: c.race == RACE.WARRIOR)
        if not warriors:
            return False
        handTargets = self.searchCards(LOCATION.hand, self.getSide(), CARD_TYPE.monster, self,
                                        lambda c: c.race == RACE.BEAST_WARRIOR and c.level <= 6
                                                  and c.canSpecialSummon())
        if not handTargets:
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

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        target = self.getLegalTarget1()
        if target:
            yield self.y_specialSummon(target)
            yield self.y_addCardData(target, atkAdd=400, effDuration=EFF_DURATION.onceForever)
        return True
