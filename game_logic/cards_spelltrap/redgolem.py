# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:redgolem
卡名:redgolem
"""
"""
1A:从卡组特殊召唤一只LV4以下的岩石族怪兽
"""
class tredgolem(Card):
    CARD_KEY="redgolem"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tredgolem_effect1)

class tredgolem_effect1(Effect):
    effType = EFF_TYPE.active

    AI_HINT = [AI_HINT.summoner]
    AI_POWER = 2

    def y_cost(self, justCheck:bool, signal):
        if not self.freeMonsterSpace():
            return False
        rockCards = self.searchCards(LOCATION.deck, self.getSide(), CARD_TYPE.monster, self,
                                      lambda c: c.race == RACE.ROCK and c.level <= 4
                                                and c.canSpecialSummon(), 1)
        if not rockCards:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        rockCards = self.searchCards(LOCATION.deck, self.getSide(), CARD_TYPE.monster, self,
                                      lambda c: c.race == RACE.ROCK and c.level <= 4
                                                and c.canSpecialSummon())
        if not rockCards:
            return False
        target = yield self.y_select1Card(rockCards, TITLE.specialSummon, canCancel=True)
        if target:
            yield self.y_specialSummon(target)
        return True
