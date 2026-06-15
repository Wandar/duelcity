# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
import random as _r
"""
CardName:T_Card_Ico_biased_cognition  【魔法】
卡图:绿色背景,发光人体剪影,六条连线指向数据节点,神经网络/大脑信息处理。
效果(AOTIP):
1A:认知偏置——自己抽2张卡,然后随机把1张手卡送入墓地(认知高效但带偏差,净+1张)。
"""

class tT_Card_Ico_biased_cognition(Card):
    CARD_KEY = "T_Card_Ico_biased_cognition"
    AUTHOR = "Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_biased_cognition_eff)

class tT_Card_Ico_biased_cognition_eff(Effect):
    effType = EFF_TYPE.active
    activateLocation = LOCATION.spellTrapZone
    AI_HINT = [AI_HINT.drawCard]
    EFF_POWER = 1

    def y_cost(self, justCheck: bool, signal):
        if len(self.game.decks[self.getSide()]) < 2: return False
        if justCheck: return True
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck: return True
        yield self.y_drawCard(self.getSide(), 2)
        myHand = self.searchCards(LOCATION.hand, self.getSide(), CARD_TYPE.all, self)
        if myHand:
            yield self.y_sendCardToGrave(_r.choice(myHand))
        return True
