# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Nightwood Stalker
卡名:夜林潜行喵
效果:1P:此卡可直接攻击;以此造成战斗伤害时自己抽1张卡。
"""

class CombatCat01(Card):
    CARD_KEY = 'CombatCat01'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(CombatCat01_e1)
        self.initEffect(CombatCat01_e2)


class CombatCat01_e1(Effect):
    # 1P:此卡可直接攻击。(可直接攻击的能力暂无钩子,登记为常驻标记效果)
    effType = EFF_TYPE.permanent
    observeSignals = (LOCATION.monsterZone, [Signal.AttachMonsterZone, Signal.DetachMonsterZone])
    AI_HINT = [AI_HINT.permanent]
    EFF_POWER = 3

    def y_signal(self, signal):
        return
        yield


class CombatCat01_e2(Effect):
    # 1P(续):以此造成战斗伤害时自己抽1张卡。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.BattleFinish])
    AI_HINT = [AI_HINT.drawCard]
    EFF_POWER = 2

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

