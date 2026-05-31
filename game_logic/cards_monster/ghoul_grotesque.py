# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Hunchbacked Ghoul
卡名:驼背食尸鬼
"""

class ghoul_grotesque(Card):
    CARD_KEY="ghoul_grotesque"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(ghoul_grotesque_DeathSpite)


"""
1T:<被战斗破坏后>:对对手造成500点LP伤害
1T:<Destroyed by battle>: Inflict 500 LP damage to your opponent.
"""
class ghoul_grotesque_DeathSpite(Effect):
    effType = EFF_TYPE.trigger

    observeSignals = (LOCATION.grave, [Signal.DestroyedByBattle])

    AI_HINT = [AI_HINT.damager]
    EFF_POWER = 1

    targetEnemy=0
    def y_cost(self, justCheck: bool, signal: Signal.DestroyedByBattle):
        if isSignal(signal, Signal.DestroyedByBattle, self.owner):
            pass
        else:
            return False
        if justCheck:
            return True

        self.targetEnemy=yield self.y_select1EnemySide()
        return True

    def y_activate(self, justCheck: bool, signal):

        if justCheck:
            return True
        yield self.y_damagePlayer(self.targetEnemy, 500)
        return True
