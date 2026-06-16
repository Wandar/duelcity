# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Spikewheel Warbot
卡名:刺轮战机
效果:1P:此卡攻击过的回合结束时,对对方场上所有怪兽各造成200点伤害。
"""

class Razor_Robot(Card):
    CARD_KEY = 'Razor Robot'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Razor_Robot_e1)


class Razor_Robot_e1(Effect):
    # 1P:此卡攻击过的回合结束时,对对方场上所有怪兽各造成200点伤害。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.BattleFinish, Signal.TurnEnds])
    AI_HINT = [AI_HINT.damager]
    EFF_POWER = 2
    _attacked = 0

    def onTurnStart(self):
        Effect.onTurnStart(self)
        self._attacked = 0

    def y_cost(self, justCheck, signal):
        if isSignal(signal, Signal.BattleFinish):
            if signal.attackerCard == self.owner:
                self._attacked = 1
            return False
        if not isSignal(signal, Signal.TurnEnds):
            return False
        if not self._attacked:
            return False
        if not self.owner.isMonsterOnField():
            return False
        enemies = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self)
        if not enemies:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        enemies = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self)
        if enemies:
            yield self.y_damageCard(enemies, 200)
        self._attacked = 0
        return True

