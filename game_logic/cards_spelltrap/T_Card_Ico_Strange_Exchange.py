# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_Strange_Exchange
卡名:诡异交换
"""

#########################my

"""
1A:双方从手牌各选1张卡交换,效果结算后各自成为对方的卡
"""

class tT_Card_Ico_Strange_Exchange(Card):
    CARD_KEY="T_Card_Ico_Strange_Exchange"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_Strange_Exchange_effect1)

class tT_Card_Ico_Strange_Exchange_effect1(Effect):
    effType = EFF_TYPE.active


    AI_HINT = [AI_HINT.drawCard]
    AI_POWER = 1

    enemy = 0
    def y_cost(self, justCheck:bool, signal):
        myHand = self.game.hands[self.getSide()]
        if not myHand:
            return
        if justCheck:
            return True
        self.enemy = yield self.y_select1EnemySide()
        if not self.game.hands[self.enemy]:
            return
        return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        myHand = self.game.hands[self.getSide()]
        enemyHand = self.game.hands[self.enemy]
        myPick = yield self.y_select1Card(myHand, TITLE.target, side=self.getSide(), canCancel=False)
        enemyPick = yield self.y_select1Card(enemyHand, TITLE.target, side=self.enemy, canCancel=False)
        # pseudo: swap hand-cards between players
        if myPick and enemyPick:
            yield self.y_swapHandCards(myPick, enemyPick)
