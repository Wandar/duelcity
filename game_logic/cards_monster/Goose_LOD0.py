# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Startled Goose
卡名:嘎嘎惊鹅
效果:1I:<手牌效果:对方特殊召唤怪兽时>:把此卡特殊召唤。
"""

class Goose_LOD0(Card):
    CARD_KEY = 'Goose_LOD0'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Goose_LOD0_e1)


class Goose_LOD0_e1(Effect):
    # 1I:<手牌效果:对方特殊召唤怪兽时>:把此卡特殊召唤。
    effType = EFF_TYPE.instant
    observeSignals = (LOCATION.hand, [Signal.SpecialSummon, Signal.SpecialSummonMultiCards])
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 2

    def y_cost(self, justCheck, signal):
        if not (isSignal(signal, Signal.SpecialSummon) or isSignal(signal, Signal.SpecialSummonMultiCards)):
            return False
        if self.owner.location != LOCATION.hand:
            return False
        scard = getattr(signal, "card", None)
        if scard is not None and self.checkAlly(scard):
            return False
        if scard is None:
            clist = getattr(signal, "cardList", None) or []
            if clist and self.checkAlly(clist[0]):
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

