# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Storm Wyvern
卡名:风暴亚龙
效果:1A:[把此卡解放]:把对方场上1只怪兽返回持有者手牌。
"""

class Fantasy_Dragon_Blue(Card):
    CARD_KEY = 'Fantasy Dragon-Blue'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Fantasy_Dragon_Blue_e1)


class Fantasy_Dragon_Blue_e1(Effect):
    # 1A:[把此卡解放]:把对方场上1只怪兽返回持有者手牌。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        enemies = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self)
        if not enemies:
            return False
        if justCheck:
            return True
        t = yield self.y_select1Card(enemies, TITLE.returnToHand, canCancel=True)
        if not t:
            return False
        successNum = yield self.y_tributeCard(self.owner)
        if not successNum:
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

