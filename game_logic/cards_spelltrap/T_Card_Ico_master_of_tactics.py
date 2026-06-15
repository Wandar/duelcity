# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_master_of_tactics  【魔法】
卡图:蓝灰背景,黑色棋盘,蓝棋红棋分立,中间白色闪电箭头,战术博弈。
效果(AOTIP):
1A:战术调度——自己场上每有1只怪兽,自己抽1张卡(最多3张)。
"""

class tT_Card_Ico_master_of_tactics(Card):
    CARD_KEY = "T_Card_Ico_master_of_tactics"
    AUTHOR = "Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_master_of_tactics_eff)

class tT_Card_Ico_master_of_tactics_eff(Effect):
    effType = EFF_TYPE.active
    activateLocation = LOCATION.spellTrapZone
    AI_HINT = [AI_HINT.drawCard]
    EFF_POWER = 2

    def y_cost(self, justCheck: bool, signal):
        myMons = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self)
        if not myMons: return False
        if not self.game.decks[self.getSide()]: return False
        if justCheck: return True
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck: return True
        cnt = len(self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self))
        n = min(3, cnt, len(self.game.decks[self.getSide()]))
        if n > 0:
            yield self.y_drawCard(self.getSide(), n)
        return True
