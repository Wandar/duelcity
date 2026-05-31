# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Luminous Wing
卡名:萤光舞翼
"""

class GiantBeetle(Card):
    CARD_KEY = "GiantBeetle"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(GiantBeetle_HarvestCrush)


"""
1T:<战斗效果>:此卡战斗破坏对方怪兽后,抽取1张牌
"""
class GiantBeetle_HarvestCrush(Effect):
    effType = EFF_TYPE.trigger

    observeSignals = (LOCATION.monsterZone, [Signal.BattleFinish])

    AI_HINT = [AI_HINT.drawCard]
    EFF_POWER = 2

    def y_cost(self, justCheck: bool, signal: Signal.BattleFinish):
        if not isSignal(signal, Signal.BattleFinish):
            return False
        if signal.attackerCard != self.owner:
            return False
        if signal.receiverCard is None:
            return False
        # 接收方已被战斗破坏（已离场）
        if signal.receiverCard.isMonsterOnField():
            return False

        if justCheck:
            return True
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck:
            return True

        yield self.y_drawCard(self.getSide(), 1)
        return True
