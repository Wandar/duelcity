# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Departure Goat
卡名:启程山羊
效果:1T:此卡直接攻击造成伤害时,自己抽1张卡。
"""

class Goat_LOD0(Card):
    CARD_KEY = 'Goat_LOD0'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Goat_LOD0_e1)


class Goat_LOD0_e1(Effect):
    # 1T:此卡直接攻击造成伤害时,自己抽1张卡。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.BattleFinish])
    AI_HINT = [AI_HINT.drawCard]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.BattleFinish):
            return False
        if signal.attackerCard != self.owner:
            return False
        if signal.battleType != BATTLE_TYPE.directAttack:
            return False
        if len(self.game.decks[self.getSide()]) < 1:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        yield self.y_drawCard(self.getSide(), 1)
        return True

