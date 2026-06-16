# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Catfish
卡名:鲶鱼
效果:1I:<手牌效果:对方发动魔法卡时>:把此卡以守备表示特殊召唤。
"""

class Catfish_LOD0(Card):
    CARD_KEY = 'Catfish_LOD0'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Catfish_LOD0_e1)


class Catfish_LOD0_e1(Effect):
    # 1I:<手牌效果:对方发动魔法卡时>:把此卡以守备表示特殊召唤。
    effType = EFF_TYPE.instant
    observeSignals = (LOCATION.hand, [Signal.BeforeActivateEffect, Signal.BeforeActivateEffectOnField])
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 2

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.BeforeActivateEffect):
            return False
        if self.owner.location != LOCATION.hand:
            return False
        if getattr(signal, "cardType", 0) & CARD_TYPE.spell == 0:
            return False
        scard = getattr(signal, "card", None)
        if scard is not None and self.checkAlly(scard):
            return False
        if self.freeMonsterSpace() == 0:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        yield self.y_specialSummon(self.owner, form=FORM.defence)
        return True

