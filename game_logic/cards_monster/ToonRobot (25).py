# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Blue Armor Patrol Droid
卡名:蓝装巡逻机
效果:1T:<召唤时>:确认对方1张盖卡或手牌;若为陷阱,可将其破坏。
"""

class ToonRobot_25(Card):
    CARD_KEY = 'ToonRobot (25)'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(ToonRobot_25_e1)


class ToonRobot_25_e1(Effect):
    # 1T:<召唤时>:确认对方1张盖卡或手牌;若为陷阱,可将其破坏。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.spellDestroyer]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        pool = self.searchCards(LOCATION.spellTrapZone | LOCATION.hand, self.getEnemySideTuple(), CARD_TYPE.all, None)
        if not pool:
            return False
        if justCheck:
            return True
        chosen = yield self.y_select1Card(pool, TITLE.target, self.getSide(), canCancel=True)
        if not chosen:
            return False
        self.saveTarget1(chosen)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1()
        if not t:
            return False
        if t.isTrap():
            ok = yield self.y_showYesNoPopUp(TITLE.destroy, TITLE.destroy, self.getSide())
            if ok == 0:
                yield self.y_destroyCard(t)
        return True

