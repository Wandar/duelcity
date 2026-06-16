# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Tyrant Dragon Rex
卡名:暴君龙王
效果:1P:对方回合开始时,对方场上攻击力最低的1只怪兽返回持有者手牌。
"""

class dragonrex(Card):
    CARD_KEY = 'dragonrex'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(dragonrex_e1)


class dragonrex_e1(Effect):
    # 1P:对方回合开始时,对方场上攻击力最低的1只怪兽返回持有者手牌。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.StandbyPhase])
    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.StandbyPhase):
            return False
        if self.game.whoseTurn == self.getSide():
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
        if not enemies:
            return False
        weakest = min(enemies, key=lambda c: c.atk)
        yield self.y_returnCardToHand(weakest)
        return True

