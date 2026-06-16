# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Little Log
卡名:小木桩
效果:1P:此卡不能攻击。2T:守备表示的此卡被攻击时,自己抽1张卡。
"""

class StumpEnt_Autumn(Card):
    CARD_KEY = 'StumpEnt_Autumn'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(StumpEnt_Autumn_e1)
        self.initEffect(StumpEnt_Autumn_e2)


class StumpEnt_Autumn_e1(Effect):
    # 1P:此卡不能攻击。(以攻击次数置0近似实现)
    effType = EFF_TYPE.permanent
    observeSignals = (LOCATION.monsterZone, [Signal.AttachMonsterZone, Signal.DetachMonsterZone])
    AI_HINT = [AI_HINT.permanent]
    EFF_POWER = 0

    def y_signal(self, signal):
        if isSignal(signal, Signal.DetachMonsterZone, self.owner):
            yield self.y_removeBuffEffectSource(self.owner, self.effUniID)
            return
        if not self.owner.isMonsterOnField():
            return
        yield self.y_changeCardData(self.owner, newAttackTimes=0,
                                    effDuration=EFF_DURATION.fromSource, uniqueSourceID=self.effUniID)


class StumpEnt_Autumn_e2(Effect):
    # 2T:守备表示的此卡被攻击时,自己抽1张卡。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.RequestBattle])
    AI_HINT = [AI_HINT.drawCard]
    EFF_POWER = 2

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.RequestBattle):
            return False
        if signal.receiverCard != self.owner:
            return False
        if self.owner.form not in (FORM.defence, FORM.defenceSet):
            return False
        if len(self.game.decks[self.getSide()]) < 1:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        yield self.y_drawCard(self.getSide(), 1)
        return True

