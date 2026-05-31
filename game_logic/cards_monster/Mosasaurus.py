# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Mosasaurus
卡名:沧龙
"""

class Mosasaurus(Card):
    CARD_KEY = "Mosasaurus"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Mosasaurus_DeepSeaDread)


"""
1T:<被战斗破坏时>:对手下回合不能对我方玩家进行直接攻击。
1T:<After this card is destroyed by battle>:Your opponent cannot attack your Life Points directly during their next turn.
"""
class Mosasaurus_DeepSeaDread(Effect):
    effType = EFF_TYPE.trigger

    observeSignals = (LOCATION.grave, [Signal.DestroyedByBattle])

    AI_HINT = [AI_HINT.blockNewMonster]
    EFF_POWER = 2

    def y_cost(self, justCheck: bool, signal):
        if not isSignal(signal, Signal.DestroyedByBattle, self.owner):
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck:
            return True

        yield self.y_addPlayerBuff(
            self.getEnemySideTuple(),
            PLAYER_BUFF.cantDirectAttack,
            EFF_DURATION.utilNextTurnEnds,
        )
        return True
