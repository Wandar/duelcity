# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Desert Boulder Colossus
卡名:沙石巨像
"""

class Prefab_Golem_Desert(Card):
    CARD_KEY="Prefab_Golem_Desert"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(Prefab_Golem_Desert_e1)


"""
1T:<被破坏后>:从卡组把最多2只等级2以下的岩石族怪兽以守备表示特殊召唤。
"""
class Prefab_Golem_Desert_e1(Effect):
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.grave, [Signal.Destroyed])
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 4

    def y_cost(self, justCheck, signal):
        # this card was the one destroyed -> it now sits in the grave
        if not isSignal(signal, Signal.Destroyed, self.owner):
            return False

        def isTarget(card):
            return card.race == RACE.ROCK and card.level <= 2

        targets = self.searchCards(LOCATION.deck, self.getSide(), CARD_TYPE.monster, self, isTarget)
        if not targets:
            return False
        if self.freeMonsterSpace() == 0:
            return False
        if justCheck:
            return True

        maxNum = min(2, self.freeMonsterSpace(), len(targets))
        chosen = yield self.y_selectCards(targets, TITLE.specialSummon, minNum=1, maxNum=maxNum)
        if not chosen:
            return False
        self.saveTarget1(chosen)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        targets = self._getLegalTargetList1(False)
        if not targets:
            return False
        yield self.y_specialSummon(targets, form=FORM.defence)
        return True
