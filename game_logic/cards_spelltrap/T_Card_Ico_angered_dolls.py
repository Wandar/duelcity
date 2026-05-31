# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_angered_dolls
卡名:愤怒玩偶
"""

#########################my

"""
1A:选择场上一只LV4以下的恶魔族怪兽,从卡组·手牌额外召唤最多两张同名卡
"""

class tT_Card_Ico_angered_dolls(Card):
    CARD_KEY="T_Card_Ico_angered_dolls"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_angered_dolls_effect1)

class tT_Card_Ico_angered_dolls_effect1(Effect):
    effType = EFF_TYPE.active

    observeSignals = (LOCATION.monsterZone,[Signal.NormalSummon])

    AI_HINT = []
    AI_POWER = 1

    def y_cost(self,justCheck:bool,signal):
        # TODO: implement cost
        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal):
        # TODO: implement effect
        if justCheck:
            return True
        yield from ()
