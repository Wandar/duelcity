# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Moth
卡名:蛾
"""

class Moth(Card):
    CARD_KEY = "Moth"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Moth_InheritedSwarm)



"""
1T:<被战斗破坏时>:可以从卡组把1只攻击力1500以下的炎属性怪兽攻击表示特殊召唤。
1OT:<When destroyed by battle>: Special Summon 1 FIRE monster with 1500 ATK or less from your Deck in Attack Position.
"""
class Moth_InheritedSwarm(Effect):
    effType = EFF_TYPE.optionalTrigger

    observeSignals = (LOCATION.grave, [Signal.DestroyedByBattle])

    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 3

    def y_cost(self, justCheck: bool, signal):
        if not isSignal(signal, Signal.DestroyedByBattle, self.owner):
            return False

        def isTarget(card):
            return c.atk <= 1500 and c.attr == ATTR.FIRE

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
