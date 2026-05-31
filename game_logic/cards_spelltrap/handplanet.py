# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:handplanet
卡名:handplanet
"""
"""
1A:选自己场上一张盖卡转移到对方场上,然后选对方场上一张盖卡转移到自己场上
"""
class thandplanet(Card):
    CARD_KEY="handplanet"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(thandplanet_effect1)

class thandplanet_effect1(Effect):
    effType = EFF_TYPE.active

    AI_HINT = [AI_HINT.eraser]
    AI_POWER = 2

    def y_cost(self, justCheck:bool, signal):
        mySetCards = self.searchCards(LOCATION.spellTrapZone, self.getSide(), CARD_TYPE.all, self,
                                       lambda c: c.isSet)
        enemySetCards = self.searchCards(LOCATION.spellTrapZone, self.getEnemySideTuple(),
                                          CARD_TYPE.all, self, lambda c: c.isSet)
        if not mySetCards or not enemySetCards:
            return False
        if justCheck:
            return True
        myCard = yield self.y_select1Card(mySetCards, TITLE.target, canCancel=True)
        enemyCard = yield self.y_select1Card(enemySetCards, TITLE.target, canCancel=True)
        if myCard and enemyCard:
            self.saveTarget1(myCard)
            self.saveTarget2(enemyCard)
            return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        myCard = self.getLegalTarget1()
        enemyCard = self.getLegalTarget2()
        if myCard:
            yield self.y_moveCardToZone(myCard, LOCATION.spellTrapZone,
                                        self.getEnemySideTuple()[0])
        if enemyCard:
            yield self.y_moveCardToZone(enemyCard, LOCATION.spellTrapZone, self.getSide())
        return True
