# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:47lightning
卡名:47lightning
"""

"""
1AI:[丢弃一张手牌]:当对方召唤怪兽时,选场上一张卡破坏
"""

class t47lightning(Card):
    CARD_KEY="47lightning"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(t47lightning_effect1)

class t47lightning_effect1(Effect):
    effType = EFF_TYPE.optionalInstant+EFF_TYPE.active

    observeSignals = (LOCATION.spellTrapZone,[Signal.Summon])

    AI_HINT = [AI_HINT.eraser]
    AI_POWER = 1
    def y_cost(self,justCheck:bool,signal:Signal.Summon):
        if isSignal(signal,Signal.PlayerActivate):
            pass
        else:
            if isSignal(signal,Signal.Summon) and signal.card.side in self.getEnemySideTuple():
                pass
            else:
                return

        myHands=self.game.hands[self.getSide()]
        if not myHands:
            return

        allCars=self.searchCards(LOCATION.mask_onField,affectSource=self)
        allCars.remove(self.owner)

        if not allCars:
            return

        if justCheck:
            return True

        sendHand=yield self.y_select1Card(myHands,TITLE.sendToGrave,canCancel=True)
        destroyCard=yield self.y_select1Card(allCars,TITLE.destroy,canCancel=True)

        if sendHand and destroyCard:
            yield self.y_sendCardToGrave(sendHand)

            self.saveTarget1(destroyCard)
            return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True

        target=self.getLegalTarget1()
        if target:
            yield self.y_destroyCard(target)
