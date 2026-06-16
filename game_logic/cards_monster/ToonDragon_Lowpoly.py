# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Sproutling Sky Dragon
卡名:豆芽小飞龙
效果:1OT:<我方回合结束时>[献祭此卡]:从手牌把1只LV6以下龙族怪兽特殊召唤。
"""

class ToonDragon_Lowpoly(Card):
    CARD_KEY = 'ToonDragon_Lowpoly'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(ToonDragon_Lowpoly_e1)


class ToonDragon_Lowpoly_e1(Effect):
    # 1OT:<我方回合结束时>[献祭此卡]:从手牌把1只LV6以下龙族怪兽特殊召唤。
    effType = EFF_TYPE.optionalTrigger
    observeSignals = (LOCATION.monsterZone, [Signal.TurnEnds])
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.TurnEnds):
            return False
        if self.game.whoseTurn != self.getSide():
            return False
        if not self.owner.isMonsterOnField():
            return False
        def isTarget(c):
            return c.race == RACE.DRAGON and c.level <= 6
        targets = self.searchCards(LOCATION.hand, self.getSide(), CARD_TYPE.monster, self, isTarget)
        if not targets:
            return False
        if justCheck:
            return True
        chosen = yield self.y_select1Card(targets, TITLE.specialSummon, canCancel=True)
        if not chosen:
            return False
        successNum = yield self.y_tributeCard(self.owner)
        if not successNum:
            return False
        self.saveTarget1(chosen)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1()
        if not t or self.freeMonsterSpace() == 0:
            return False
        yield self.y_specialSummon(t)
        return True

