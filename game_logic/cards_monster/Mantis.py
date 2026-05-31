# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Mantis
卡名:螳螂
"""

class Mantis(Card):
    CARD_KEY = "Mantis"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Mantis_InheritedSwarm)



"""
1OT:<被战斗破坏时>:从卡组把1只攻击力1500以下的地属性怪兽攻击表示特殊召唤。
1OT:<When destroyed by battle>: Special Summon 1 EARTH monster with 1500 ATK or less from your Deck in Attack Position.
"""
class Mantis_InheritedSwarm(Effect):
    effType = EFF_TYPE.optionalTrigger

    observeSignals = (LOCATION.grave, [Signal.DestroyedByBattle])

    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 3

    def y_cost(self, justCheck: bool, signal):
        if not isSignal(signal, Signal.DestroyedByBattle, self.owner):
            return False

        def isTarget(card):
            return c.atk <= 1500 and c.attr == ATTR.EARTH

        targets = self.searchCards(
            LOCATION.deck, self.getSide(), CARD_TYPE.monster, self, isTarget
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
