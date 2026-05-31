# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Fire Dragon
卡名:火龙
"""

class FireDragonRed(Card):
    CARD_KEY = "FireDragonRed"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(FireDragonRed_EmberRetaliation)


"""
1I:<场上效果>:我方怪兽被战斗破坏时,对对手造成300点LP伤害。
1I:<When a monster on your field is destroyed by battle>:Inflict 300 LP damage to your opponent.
"""
class FireDragonRed_EmberRetaliation(Effect):
    effType = EFF_TYPE.instant

    observeSignals = (LOCATION.monsterZone, [Signal.BattleFinish])

    AI_HINT = [AI_HINT.damager]
    EFF_POWER = 1

    def y_activate(self, justCheck: bool, signal: Signal.BattleFinish):
        if not isSignal(signal, Signal.BattleFinish):
            return False
        if signal.receiverCard is None:
            return False
        # 接收方是我方怪兽且已被战斗破坏（离场）
        if signal.receiverCard.side not in self.getAllySideTuple():
            return False
        if signal.receiverCard.isMonsterOnField():
            return False
        if not self.owner.isMonsterOnField():
            return False

        if justCheck:
            return True

        yield self.y_damagePlayer(self.getEnemySideTuple(), 300)
        return True
