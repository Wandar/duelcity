# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_overclock
卡名:超频
"""

#########################my

"""
1A:[Cost:支付1000基本分]:自己从卡组抽2张,本回合结束时自己丢弃1张手牌
"""

class tT_Card_Ico_overclock(Card):
    CARD_KEY="T_Card_Ico_overclock"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_overclock_effect1)

class tT_Card_Ico_overclock_effect1(Effect):
    effType = EFF_TYPE.active


    AI_HINT = [AI_HINT.drawCard]
    AI_POWER = 1

    def y_cost(self, justCheck:bool, signal):
        if self.game.getPlayerLP(self.getSide()) <= 1000:
            return
        if self.getDeckLeftNum() < 1:
            return
        if justCheck:
            return True
        yield self.y_damagePlayer(self.getSide(), 1000)
        return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        yield self.y_drawCard(self.getSide(), 2)
        # pseudo: schedule end-of-turn hand discard
        yield self.y_scheduleEndTurnAction(self.getSide(), action='discard1Hand')
