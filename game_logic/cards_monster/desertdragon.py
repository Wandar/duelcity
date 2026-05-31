# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Flaming Sand Dragon
卡名:烈焰沙龙
"""

class desertdragon(Card):
    CARD_KEY = "desertdragon"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(desertdragon_SandstormFury)


"""
1T:<场上效果>:这张卡战斗破坏对方怪兽送去墓地的场合发动。{ATK}+700。
1T:<Battle effect>:After this card destroys a monster by battle, this card gains 700 ATK (permanent).
"""
class desertdragon_SandstormFury(Effect):
    effType = EFF_TYPE.trigger

    observeSignals = (LOCATION.monsterZone, [Signal.BattleFinish])

    AI_HINT = [AI_HINT.addAtk]
    EFF_POWER = 3

    def y_cost(self, justCheck: bool, signal: Signal.BattleFinish):
        if not isSignal(signal, Signal.BattleFinish):
            return False
        if signal.attackerCard != self.owner:
            return False
        if signal.receiverCard is None:
            return False
        if signal.receiverCard.isMonsterOnField():
            return False
        if not self.owner.isMonsterOnField():
            return False

        if justCheck:
            return True
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck:
            return True

        yield self.y_addCardData(
            self.owner,
            attackAdd=700,
            effDuration=EFF_DURATION.permanent,
        )
        return True
