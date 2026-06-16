# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Mantis
卡名:螳螂
效果:1T:<对方怪兽攻击自己的其他昆虫族怪兽后>:此卡立即直接攻击对方玩家。
"""

class Mantis(Card):
    CARD_KEY = 'Mantis'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Mantis_e1)


class Mantis_e1(Effect):
    # 1T:<对方怪兽攻击自己的其他昆虫族怪兽后>:此卡立即直接攻击对方玩家。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.BattleFinish])
    AI_HINT = [AI_HINT.battleBenefit]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.BattleFinish):
            return False
        attacker = signal.attackerCard
        receiver = signal.receiverCard
        if attacker is None or receiver is None:
            return False
        if not (attacker.side in self.getEnemySideTuple()):
            return False
        if receiver == self.owner or not self.checkAlly(receiver) or receiver.race != RACE.INSECT:
            return False
        if not self.owner.isMonsterOnField():
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        if not self.owner.isMonsterOnField():
            return False
        enemySide = self.getEnemySideTuple()[0]
        yield self.y_battleByEffect(self.owner, enemySide)
        return True

