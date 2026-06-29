# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Flaming Sand Dragon
卡名:烈焰沙龙
效果:1T:<召唤时>:破坏对方场上1张魔法·陷阱卡。2T:<被破坏时>:从手牌把1只等级5以下的龙族怪兽特殊召唤。
"""

class desertdragon(Card):
    CARD_KEY = "desertdragon"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(desertdragon_e1)
        self.initEffect(desertdragon_e2)


class desertdragon_e1(Effect):
    # 1T:<召唤时>:破坏对方场上1张魔法·陷阱卡。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.spellDestroyer]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        targets = self.searchCards(LOCATION.spellTrapZone, self.getEnemySideTuple(),
                                   CARD_TYPE.all, self)
        if not targets:
            return False
        if justCheck:
            return True
        chosen = yield self.y_select1Card(targets, TITLE.destroy, canCancel=False)
        if not chosen:
            return False
        self.saveTarget1(chosen)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        target = self.getLegalTarget1()
        if not target:
            return False
        yield self.y_destroyCard(target)
        return True


class desertdragon_e2(Effect):
    # 2T:<被破坏时>:从手牌把1只等级5以下的龙族怪兽特殊召唤。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.grave, [Signal.Destroyed])
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Destroyed, self.owner):
            return False
        def isTarget(c):
            return c.race == RACE.DRAGON and c.level <= 5
        targets = self.searchCards(LOCATION.hand, self.getSide(), CARD_TYPE.monster, self, isTarget)
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

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1(checkLocationChange=False)
        if not t or self.freeMonsterSpace() == 0:
            return False
        yield self.y_specialSummon(t)
        return True
