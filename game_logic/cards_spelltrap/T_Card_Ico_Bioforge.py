# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_Bioforge
卡名:生体锻造
effect:
效果:1A:从卡组随机发现一只战士族怪兽,特殊召唤到自己场上
"""

class tT_Card_Ico_Bioforge(Card):
    CARD_KEY = "T_Card_Ico_Bioforge"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(tT_Card_Ico_Bioforge_effect1)


class tT_Card_Ico_Bioforge_effect1(Effect):
    # 1A:从卡组随机发现一只战士族怪兽,特殊召唤到自己场上
    effType = EFF_TYPE.active
    AI_HINT = [AI_HINT.searchMonster]
    AI_POWER = 1

    def y_cost(self, justCheck, signal):
        if self.freeMonsterSpace() == 0:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        picked = yield self.y_discoverCard(side=self.getSide(), race=RACE.WARRIOR,
                                           cardType=CARD_TYPE.monster, count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked, form=FORM.attack)
        return True
