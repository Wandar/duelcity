# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Jumping Raccoon
卡名:跳跳浣熊
"""

class toon_Raccoon(Card):
    CARD_KEY="toon_Raccoon"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(toon_Raccoon_e1)


"""
1A:[把场上的此卡返回手牌]:自己抽1张卡。
"""
class toon_Raccoon_e1(Effect):
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.drawCard]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if justCheck:
            return True
        successNum = yield self.y_returnCardToHand(self.owner)
        return successNum != 0

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        yield self.y_drawCard(self.getSide())
        return True
