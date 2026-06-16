# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Brachiosaurus
卡名:腕龙
效果:1T:<当此卡变为守备表示>:从手牌把1只等级3以下的恐龙族怪兽特殊召唤。
"""

class Brachiosaurus(Card):
    CARD_KEY = 'Brachiosaurus'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Brachiosaurus_e1)


class Brachiosaurus_e1(Effect):
    # 1T:<当此卡变为守备表示>:从手牌把1只等级3以下的恐龙族怪兽特殊召唤。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.CardChangeForm])
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.CardChangeForm):
            return False
        if getattr(signal, "card", None) != self.owner:
            return False
        if self.owner.form not in (FORM.defence, FORM.defenceSet):
            return False
        def isTarget(c):
            return c.race == RACE.DINOSAUR and c.level <= 3
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
        t = self.getLegalTarget1()
        if not t:
            return False
        yield self.y_specialSummon(t)
        return True

