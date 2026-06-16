# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Redfeather Falcon
卡名:赤羽隼
效果:1T:此卡直接攻击造成伤害时,破坏对方场上1张魔法·陷阱卡。
"""

class Eagle_Brown(Card):
    CARD_KEY = 'Eagle_Brown'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Eagle_Brown_e1)


class Eagle_Brown_e1(Effect):
    # 1T:此卡直接攻击造成伤害时,破坏对方场上1张魔法·陷阱卡。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.BattleFinish])
    AI_HINT = [AI_HINT.spellDestroyer]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.BattleFinish):
            return False
        if signal.attackerCard != self.owner:
            return False
        if signal.battleType != BATTLE_TYPE.directAttack:
            return False
        enemyST = self.searchCards(LOCATION.spellTrapZone, self.getEnemySideTuple(), CARD_TYPE.all, self)
        if not enemyST:
            return False
        if justCheck:
            return True
        t = yield self.y_select1Card(enemyST, TITLE.destroy, canCancel=True)
        if not t:
            return False
        self.saveTarget1(t)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1()
        if not t:
            return False
        yield self.y_destroyCard(t)
        return True

