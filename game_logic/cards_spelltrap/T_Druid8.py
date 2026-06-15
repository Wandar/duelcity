# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Druid8  【魔法】
卡图:黑暗背景,深红大花盛开,花瓣边缘绿色荧光,花蕊黄绿亮光,原始生命力。
效果(AOTIP):
1A:生命绽放——自己回复1000基本分,然后自己抽1张卡。
"""

class tT_Druid8(Card):
    CARD_KEY = "T_Druid8"
    AUTHOR = "Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Druid8_eff)

class tT_Druid8_eff(Effect):
    effType = EFF_TYPE.active
    activateLocation = LOCATION.spellTrapZone
    AI_HINT = [AI_HINT.recoverLP, AI_HINT.drawCard]
    EFF_POWER = 2

    def y_cost(self, justCheck: bool, signal):
        if justCheck: return True
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck: return True
        yield self.y_healPlayer(self.getSide(), 1000)
        if self.game.decks[self.getSide()]:
            yield self.y_drawCard(self.getSide(), 1)
        return True
