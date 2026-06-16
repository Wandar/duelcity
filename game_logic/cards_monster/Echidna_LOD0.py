# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Echidna
卡名:针鼹
效果:1T:<被攻击时>:此卡变为守备表示,这次战斗中此卡不会被破坏。
"""

class Echidna_LOD0(Card):
    CARD_KEY = 'Echidna_LOD0'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Echidna_LOD0_e1)


class Echidna_LOD0_e1(Effect):
    # 1T:<被攻击时>:此卡变为守备表示,这次战斗中此卡不会被破坏。
    # NOTE: "不会被破坏" 以本次战斗内临时巨幅提升守备力近似实现。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.RequestBattle])
    AI_HINT = [AI_HINT.battleBenefit]
    EFF_POWER = 2

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.RequestBattle):
            return False
        if signal.receiverCard != self.owner:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        yield self.y_changeForm(self.owner, FORM.defence)
        yield self.y_changeCardData(self.owner, newDefence=99999, effDuration=EFF_DURATION.utilBattleEnds)
        return True

