# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Dreamy Sea Dragon
卡名:梦幻海龙
效果:1T:<召唤·特殊召唤时>:把对方场上1只怪兽返回持有者手牌。
"""

class LDSea_Toon(Card):
    CARD_KEY = 'LDSea Toon'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(LDSea_Toon_e1)


class LDSea_Toon_e1(Effect):
    # 1T:<召唤·特殊召唤时>:把对方场上1只怪兽返回持有者手牌。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        enemies = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self)
        if not enemies:
            return False
        if justCheck:
            return True
        t = yield self.y_select1Card(enemies, TITLE.returnToHand, canCancel=True)
        if not t:
            return False
        self.saveTarget1(t)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1()
        if not t:
            return False
        yield self.y_returnCardToHand(t)
        return True

