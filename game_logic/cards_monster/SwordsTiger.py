# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Swords Tiger
卡名:剑虎
效果:1T:[不限次数]:此卡战斗破坏对方怪兽后,此卡可以再进行1次攻击。
"""

class SwordsTiger(Card):
    CARD_KEY = 'SwordsTiger'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(SwordsTiger_e1)


class SwordsTiger_e1(Effect):
    # 1T:[不限次数]:此卡战斗破坏对方怪兽后,此卡可以再进行1次攻击。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.BattleFinish])
    AI_HINT = [AI_HINT.battleBenefit]
    EFF_POWER = 4
    countLimit = COUNT_LIMIT.unlimited

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.BattleFinish):
            return False
        if signal.attackerCard != self.owner:
            return False
        rc = signal.receiverCard
        if rc is None or rc.isMonsterOnField():
            return False
        if not self.owner.isMonsterOnField():
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        yield self.y_addCardData(self.owner, attackTimesAdd=1, effDuration=EFF_DURATION.utilTurnEnds)
        return True

