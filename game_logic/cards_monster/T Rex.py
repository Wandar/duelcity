# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T Rex
卡名:暴龙
"""

class T_Rex(Card):
    CARD_KEY = "T Rex"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(T_Rex_ApexFangs)


"""
1T:<战斗效果>:战斗破坏对方怪兽后,{ATK}+700。
1T: <Field effect>: When this card destroys an opponent's monster by battle and sends it to the Graveyard, this card gains 700 ATK.
"""
class T_Rex_ApexFangs(Effect):
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
