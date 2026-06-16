# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Sunlit Winged Sunflower Fairy
卡名:向阳翼花妖
效果:1T:<被破坏后>:从卡组把1只「向阳翼花王」特殊召唤。2T:<召唤时>:发现1张植物族怪兽卡。
"""

class Sunflower_Fairy(Card):
    CARD_KEY = 'Sunflower Fairy'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Sunflower_Fairy_e1)
        self.initEffect(Sunflower_Fairy_e2)


class Sunflower_Fairy_e1(Effect):
    # 1T:<被破坏后>:从卡组把1只「向阳翼花王」特殊召唤。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.grave, [Signal.Destroyed])
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Destroyed, self.owner):
            return False
        def isTarget(c):
            return c.cardKey == "Sunflora Pixie"
        targets = self.searchCards(LOCATION.deck, self.getSide(), CARD_TYPE.monster, self, isTarget)
        if not targets:
            return False
        if self.freeMonsterSpace() == 0:
            return False
        if justCheck:
            return True
        self.saveTarget1(targets[0])
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1(checkLocationChange=False)
        if not t:
            return False
        yield self.y_specialSummon(t)
        return True


class Sunflower_Fairy_e2(Effect):
    # 2T:<召唤时>:发现1张植物族怪兽卡。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.searchMonster]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        yield self.y_discoverCard(side=self.getSide(), race=RACE.PLANT,
                                  cardType=CARD_TYPE.monster, count=3, canCancel=True)
        return True

