# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_loop
卡名:循环
"""

#########################my

"""
1A:将自己场上1张魔法卡返回手牌,然后自己从卡组抽1张
"""

class tT_Card_Ico_loop(Card):
    CARD_KEY="T_Card_Ico_loop"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_loop_effect1)

class tT_Card_Ico_loop_effect1(Effect):
    effType = EFF_TYPE.active


    AI_HINT = [AI_HINT.drawCard]
    AI_POWER = 1

    def y_cost(self, justCheck:bool, signal):
        mySpells = self.searchCards(LOCATION.spellTrapZone, self.getSide(), CARD_TYPE.spell, self)
        if self.owner in mySpells:
            mySpells.remove(self.owner)
        if not mySpells:
            return
        if not self.getDeckLeftNum():
            return
        if justCheck:
            return True
        target = yield self.y_select1Card(mySpells, TITLE.returnToHand, canCancel=True)
        if target:
            self.saveTarget1(target)
            return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        target = self.getLegalTarget1()
        if target:
            yield self.y_returnCardToHand(target, self.getSide())
        yield self.y_drawCard(self.getSide(), 1)
