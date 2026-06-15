# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_recycle  【魔法】
卡图:绿色背景,绿色三角循环箭头,内部蓝色能量球,四周黄色闪电,循环利用。
效果(AOTIP):
1A:循环再生——以自己墓地1张卡为对象加入手卡;再以自己被除外的1张卡为对象,送回墓地。
"""

class tT_Card_Ico_recycle(Card):
    CARD_KEY = "T_Card_Ico_recycle"
    AUTHOR = "Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_recycle_eff)

class tT_Card_Ico_recycle_eff(Effect):
    effType = EFF_TYPE.active
    activateLocation = LOCATION.spellTrapZone
    AI_HINT = [AI_HINT.earn]
    EFF_POWER = 2

    def y_cost(self, justCheck: bool, signal):
        grave = self.searchCards(LOCATION.grave, self.getSide(), CARD_TYPE.all, self)
        banished = self.searchCards(LOCATION.banish, self.getSide(), CARD_TYPE.all, self)
        if not grave and not banished: return False
        if justCheck: return True
        if grave:
            g = yield self.y_select1Card(grave, TITLE.addToHand, self.getSide(), canCancel=True)
            if g: self.saveTarget1(g)
        if banished:
            b = yield self.y_select1Card(banished, TITLE.sendToGrave, self.getSide(), canCancel=True)
            if b: self.saveTarget2(b)
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck: return True
        g = self.getLegalTarget1()
        if g:
            yield self.y_returnCardToHand(g, self.getSide())
        b = self.getLegalTarget2(checkLocationChange=False)
        if b:
            yield self.y_sendCardToGrave(b, self.getSide())
        return True
