# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Flying Demon
卡名:飞翔恶魔
效果:1T:<手牌效果:自己的怪兽被战斗破坏时>:把此卡特殊召唤。
"""

class FlyingDemonDefault(Card):
    CARD_KEY = 'FlyingDemonDefault'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(FlyingDemonDefault_e1)


class FlyingDemonDefault_e1(Effect):
    # 1T:<手牌效果:自己的怪兽被战斗破坏时>:把此卡特殊召唤。
    effType = EFF_TYPE.optionalTrigger
    observeSignals = (LOCATION.hand, [Signal.DestroyedByBattle])
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 2

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.DestroyedByBattle):
            return False
        if self.owner.location != LOCATION.hand:
            return False
        card = getattr(signal, "card", None)
        if card is None or card == self.owner or not self.checkAlly(card):
            return False
        if self.freeMonsterSpace() == 0:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        yield self.y_specialSummon(self.owner)
        return True

