# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Ankylosaurus
卡名:甲龙
"""

class Ankylosaurus(Card):
    CARD_KEY = "Ankylosaurus"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Ankylosaurus_TailSlam)


"""
1A:<战斗效果>:这张卡战斗破坏对方怪兽送去墓地时，给与对方基本分400分伤害。
1OT: <Battle effect>: When this card destroys an opponent's monster by battle and sends it to the Graveyard, inflict 400 damage to your opponent.
"""
class Ankylosaurus_TailSlam(Effect):
    effType = EFF_TYPE.optionalTrigger

    observeSignals = (LOCATION.monsterZone, [Signal.BattleFinish])

    AI_HINT = [AI_HINT.damager]
    EFF_POWER = 2

    def y_cost(self, justCheck: bool, signal: Signal.BattleFinish):
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

    def y_activate(self, justCheck: bool, signal):
        if justCheck:
            return True

        yield self.y_damagePlayer(self.getEnemySideTuple(), 400)
        return True
