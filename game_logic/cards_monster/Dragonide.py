# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Hammer Lizard
卡名:铁锤蜥蜴
"""

class Dragonide(Card):
    CARD_KEY = "Dragonide"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Dragonide_DragonCall)


"""
1OT:此卡通常召唤成功时,从墓地将1只3星以下的龙族怪兽特殊召唤。
1OT:<When this card is Normal Summoned>:Special Summon 1 Level 3 or lower DRAGON monster from your Graveyard.
"""
class Dragonide_DragonCall(Effect):
    effType = EFF_TYPE.optionalTrigger

    observeSignals = (LOCATION.monsterZone, [Signal.NormalSummon])

    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 2

    def y_cost(self, justCheck: bool, signal: Signal.NormalSummon):
        if not isSignal(signal, Signal.NormalSummon, self.owner):
            return False

        def isTarget(card):
            return card.race == RACE.DRAGON and card.level <= 3

        targets = self.searchCards(
            LOCATION.grave, self.getSide(), CARD_TYPE.monster, self, isTarget
        )
        if not targets:
            return False
        if self.freeMonsterSpace() == 0:
            return False

        if justCheck:
            return True

        chosen = yield self.y_select1Card(targets, TITLE.specialSummon, canCancel=True)
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

        yield self.y_specialSummon(target)
        return True
