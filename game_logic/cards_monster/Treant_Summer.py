# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Summer Treant
卡名:夏日树妖
效果:1T:<我方回合的结束阶段>:此卡攻击力上升300。
"""

class Treant_Summer(Card):
    CARD_KEY = 'Treant_Summer'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Treant_Summer_e1)


class Treant_Summer_e1(Effect):
    # 1T:<我方回合的结束阶段>:此卡攻击力上升300。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.TurnEnds])
    AI_HINT = [AI_HINT.enhance]
    EFF_POWER = 2
    countLimit = COUNT_LIMIT.unlimited

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.TurnEnds):
            return False
        if self.game.whoseTurn != self.getSide():
            return False
        if not self.owner.isMonsterOnField():
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        yield self.y_addCardData(self.owner, attackAdd=300, effDuration=EFF_DURATION.onceForever)
        return True
