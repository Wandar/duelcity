# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Cluck-Cluck Turkey
卡名:咯咯火鸡
效果:1T:<被战斗破坏后>:破坏此卡的怪兽变为守备表示,下个回合不能攻击。
"""

class Turkey_LOD0(Card):
    CARD_KEY = 'Turkey_LOD0'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Turkey_LOD0_e1)


class Turkey_LOD0_e1(Effect):
    # 1T:<被战斗破坏后>:破坏此卡的怪兽变为守备表示,下个回合不能攻击。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.grave, [Signal.DestroyedByBattle])
    AI_HINT = [AI_HINT.debuff]
    EFF_POWER = 2

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.DestroyedByBattle, self.owner):
            return False
        killer = getattr(signal, "reasonCard", None)
        if killer is None or not killer.isMonsterOnField():
            return False
        if justCheck:
            return True
        self.saveTarget1(killer)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1(checkLocationChange=False)
        if not t or not t.isMonsterOnField():
            return False
        yield self.y_changeForm(t, FORM.defence)
        # "下个回合不能攻击" -> 攻击次数置0至下回合结束(近似)
        yield self.y_changeCardData(t, newAttackTimes=0, effDuration=EFF_DURATION.utilNextTurnEnds)
        return True

