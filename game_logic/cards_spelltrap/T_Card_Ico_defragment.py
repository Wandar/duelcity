# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_defragment  【魔法】
卡图:绿色背景,彩色方块积木堆叠,一块橙色方块飞出,数字碎片整理。
效果(AOTIP):
1A:碎片整理——把自己手卡全部洗回卡组,然后抽出相同数量的卡。
"""

class tT_Card_Ico_defragment(Card):
    CARD_KEY = "T_Card_Ico_defragment"
    AUTHOR = "Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_defragment_eff)

class tT_Card_Ico_defragment_eff(Effect):
    effType = EFF_TYPE.active
    activateLocation = LOCATION.spellTrapZone
    AI_HINT = [AI_HINT.drawCard]
    EFF_POWER = 2

    def y_cost(self, justCheck: bool, signal):
        myHand = self.searchCards(LOCATION.hand, self.getSide(), CARD_TYPE.all, self)
        if not myHand: return False
        if justCheck: return True
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck: return True
        myHand = self.searchCards(LOCATION.hand, self.getSide(), CARD_TYPE.all, self)
        n = len(myHand)
        if myHand:
            yield self.y_returnCardToDeck(myHand, self.getSide(), RETURN_TO_DECK.shuffle)
        n = min(n, len(self.game.decks[self.getSide()]))
        if n > 0:
            yield self.y_drawCard(self.getSide(), n)
        return True
