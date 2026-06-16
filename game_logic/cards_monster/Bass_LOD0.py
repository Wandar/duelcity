# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Bass
卡名:大口鲈
效果:1T:此卡进行战斗的回合结束时,此卡返回持有者手牌。
"""

class Bass_LOD0(Card):
    CARD_KEY = 'Bass_LOD0'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Bass_LOD0_e1)


class Bass_LOD0_e1(Effect):
    # 1T:此卡进行战斗的回合结束时,此卡返回持有者手牌。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.BattleFinish, Signal.TurnEnds])
    AI_HINT = [AI_HINT.botDontUse]
    EFF_POWER = 1
    _battled = 0

    def onTurnStart(self):
        Effect.onTurnStart(self)
        self._battled = 0

    def y_cost(self, justCheck, signal):
        if isSignal(signal, Signal.BattleFinish):
            if signal.attackerCard == self.owner or signal.receiverCard == self.owner:
                self._battled = 1
            return False
        if not isSignal(signal, Signal.TurnEnds):
            return False
        if not self._battled:
            return False
        if not self.owner.isMonsterOnField():
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        yield self.y_returnCardToHand(self.owner)
        self._battled = 0
        return True

