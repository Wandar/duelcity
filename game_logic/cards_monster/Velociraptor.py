# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Velociraptor
卡名:迅猛龙
"""

class Velociraptor(Card):
    CARD_KEY = "Velociraptor"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Velociraptor_Frenzy)


"""
1OT:<战斗效果>:战斗破坏对方怪兽后,{ATK}+1000
1OT:<BattleEffect>:After destroying an opponent's monster by battle,{ATK}+1000
"""
class Velociraptor_Frenzy(Effect):
    effType = EFF_TYPE.optionalTrigger

    observeSignals = (LOCATION.monsterZone, [Signal.BattleFinish])

    AI_HINT = [AI_HINT.addAtk]
    EFF_POWER = 4

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
            attackAdd=1000,
            effDuration=EFF_DURATION.permanent,
        )
        return True
