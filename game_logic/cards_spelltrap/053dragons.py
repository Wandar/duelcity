# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:053dragons
卡名:053dragons
"""
"""
1A:如果墓地中龙族怪兽有三只以上时,随机将其中两只怪兽返回手牌
"""
class t053dragons(Card):
    CARD_KEY="053dragons"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(t053dragons_effect1)

class t053dragons_effect1(Effect):
    effType = EFF_TYPE.active

    AI_HINT = [AI_HINT.search]
    AI_POWER = 2

    def y_cost(self, justCheck:bool, signal):
        gravedragons = self.searchCards(LOCATION.grave, 0, CARD_TYPE.monster, self,
                                        lambda c: c.race == RACE.DRAGON)
        if len(gravedragons) < 3:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        gravedrags = self.searchCards(LOCATION.grave, 0, CARD_TYPE.monster, self,
                                       lambda c: c.race == RACE.DRAGON)
        import random
        targets = random.sample(gravedrags, min(2, len(gravedrags)))
        for t in targets:
            yield self.y_returnCardToHand(t)
        return True
