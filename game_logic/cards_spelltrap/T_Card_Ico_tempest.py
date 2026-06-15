# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_tempest  【魔法】
卡图:深色背景,红色大型蜈蚣状生物斜穿画面,环绕黄色闪电裂纹,风暴破坏力。
效果(AOTIP):
1A:[支付1000]:风暴肆虐——对方场上所有怪兽各受到400伤害,并对对方造成400伤害。
"""

class tT_Card_Ico_tempest(Card):
    CARD_KEY = "T_Card_Ico_tempest"
    AUTHOR = "Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_tempest_eff)

class tT_Card_Ico_tempest_eff(Effect):
    effType = EFF_TYPE.active
    activateLocation = LOCATION.spellTrapZone
    AI_HINT = [AI_HINT.damager]
    EFF_POWER = 3

    def y_cost(self, justCheck: bool, signal):
        if self.game.LPs[self.getSide()] <= 1000: return False
        if justCheck: return True
        yield self.y_damagePlayer(self.getSide(), 1000)
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck: return True
        enMons = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self)
        if enMons:
            yield self.y_damageCard(enMons, 400)
        yield self.y_damagePlayer(self.getEnemySideTuple(), 400)
        return True
