# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
import random as _r
"""
CardName:T_Card_Ico_Strange_Exchange  【魔法】
卡图:蓝色放射光,绿色手臂与粉紫手臂握手,各有白色能量环,象征奇异交换。
效果(AOTIP):
1A:奇异交换——把自己1张手卡交给对方手卡,再随机取走对方1张手卡加入自己手卡。
"""

class tT_Card_Ico_Strange_Exchange(Card):
    CARD_KEY = "T_Card_Ico_Strange_Exchange"
    AUTHOR = "Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_Strange_Exchange_eff)

class tT_Card_Ico_Strange_Exchange_eff(Effect):
    effType = EFF_TYPE.active
    activateLocation = LOCATION.spellTrapZone
    AI_HINT = [AI_HINT.debuff]
    EFF_POWER = 2

    def y_cost(self, justCheck: bool, signal):
        myHand = self.searchCards(LOCATION.hand, self.getSide(), CARD_TYPE.all, self)
        enHand = self.searchCards(LOCATION.hand, self.getEnemySideTuple(), CARD_TYPE.all, self)
        if not myHand or not enHand: return False
        if justCheck: return True
        give = yield self.y_select1Card(myHand, TITLE.returnToHand, self.getSide(), canCancel=True)
        if not give: return False
        self.saveTarget1(give)
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck: return True
        give = self.getLegalTarget1()
        es = self.getEnemySideTuple()
        if give and es:
            yield self.y_returnCardToHand(give, es[0])
        enHand = self.searchCards(LOCATION.hand, self.getEnemySideTuple(), CARD_TYPE.all, self)
        if enHand:
            yield self.y_returnCardToHand(_r.choice(enHand), self.getSide())
        return True
