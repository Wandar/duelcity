# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_multi_cast
卡名:多重施法
"""

#########################my

"""
1A:将自己墓地1张通常魔法卡除外,复制其效果并发动
"""

class tT_Card_Ico_multi_cast(Card):
    CARD_KEY="T_Card_Ico_multi_cast"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_multi_cast_effect1)

class tT_Card_Ico_multi_cast_effect1(Effect):
    effType = EFF_TYPE.active


    AI_HINT = [AI_HINT.drawCard]
    AI_POWER = 1

    def y_cost(self, justCheck:bool, signal):
        def f(c):
            return c.cardType & CARD_TYPE.spell
        pool = self.searchCards(LOCATION.graveyard, self.getSide(), CARD_TYPE.spell, self, f)
        if not pool:
            return
        if justCheck:
            return True
        target = yield self.y_select1Card(pool, TITLE.copyEffect, canCancel=True)
        if target:
            self.saveTarget1(target)
            return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        target = self.getLegalTarget1()
        if target:
            yield self.y_banishCard(target)
            # pseudo: re-trigger the target spell's first effect against this side
            yield self.y_copyAndActivateSpellEffect(target, self.getSide())
