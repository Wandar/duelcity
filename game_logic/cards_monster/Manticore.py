# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Manticore
卡名:刺尾狮
效果:1T:<召唤时>:从自己墓地把1只龙族怪兽加入手牌。2T:<此卡战斗破坏对方怪兽时>:对对方造成500伤害。
"""

class Manticore(Card):
    CARD_KEY = "Manticore"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Manticore_e1)
        self.initEffect(Manticore_e2)


class Manticore_e1(Effect):
    # 1T:<召唤时>:从自己墓地把1只龙族怪兽加入手牌。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.earn]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        def isDragon(c):
            return c.race == RACE.DRAGON
        targets = self.searchCards(LOCATION.grave, self.getSide(), CARD_TYPE.monster, self, isDragon)
        if not targets:
            return False
        if justCheck:
            return True
        chosen = yield self.y_select1Card(targets, TITLE.addToHand, canCancel=True)
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
        yield self.y_returnCardToHand(t)
        return True


class Manticore_e2(Effect):
    # 2T:<此卡战斗破坏对方怪兽时>:对对方造成500伤害。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.BattleFinish])
    AI_HINT = [AI_HINT.damager]
    EFF_POWER = 2

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.BattleFinish):
            return False
        if signal.attackerCard != self.owner:
            return False
        if signal.receiverCard is None:
            return False
        if signal.receiverCard.isMonsterOnField():
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        yield self.y_damagePlayer(self.getEnemySideTuple(), 500)
        return True
