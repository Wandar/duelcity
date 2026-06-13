# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Werecrab
卡名:蟹人
"""

class werecrab(Card):
    CARD_KEY = "werecrab"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(werecrab_TidalBoost)



"""
1T:这张卡从墓地特殊召唤成功时,选择场上1只鱼族·海龙族·水族怪兽,其等级上升1星。
1T:<FieldEffect>:When this card is Special Summoned from the Graveyard, choose 1 FISH/SEA_SERPENT/AQUA monster on the field; its Level increases by 1.
"""
class werecrab_TidalBoost(Effect):
    effType = EFF_TYPE.trigger

    observeSignals = (LOCATION.monsterZone, [Signal.SpecialSummon])

    AI_HINT = [AI_HINT.enhance]
    EFF_POWER = 2

    def y_cost(self, justCheck: bool, signal):
        if not isSignal(signal, Signal.SpecialSummon, self.owner):
            return False
        if signal.card != self.owner:
            return False
        if getattr(signal, 'fromLocation', None) != LOCATION.grave:
            return False

        def isFishLike(c):
            return c.race in (RACE.FISH, RACE.SEA_SERPENT, RACE.AQUA)

        cands = self.searchCards(LOCATION.monsterZone, -1, CARD_TYPE.monster, None, isFishLike)
        if not cands:
            return False
        if justCheck:
            return True

        chosen = yield self.y_select1Card(cands, TITLE.target, canCancel=True)
        if not chosen:
            return False
        self.saveTarget1(chosen)
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck:
            return True
        target = self.getLegalTarget1(checkLocationChange=False)
        if not target:
            return False
        yield self.y_addCardData(target, levelAdd=1, effDuration=EFF_DURATION.permanent)
        return True
