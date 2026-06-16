# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Shoebill
卡名:鲸头鹳
效果:1P:此卡召唤·特殊召唤的回合和下个回合不能攻击。
"""

class Shoebill_LOD0(Card):
    CARD_KEY = 'Shoebill_LOD0'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Shoebill_LOD0_e1)


class Shoebill_LOD0_e1(Effect):
    # 1P:此卡召唤·特殊召唤的回合和下个回合不能攻击。(以攻击次数置0近似)
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.botDontUse]
    EFF_POWER = 0

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        yield self.y_changeCardData(self.owner, newAttackTimes=0,
                                    effDuration=EFF_DURATION.utilNextTurnEnds)
        return True

