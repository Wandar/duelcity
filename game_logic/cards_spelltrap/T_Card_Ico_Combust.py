# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_Combust
卡名:自爆引燃
"""

#########################my

"""
1I:对方怪兽攻击时,破坏自己场上1只怪兽,给与对方800伤害
"""

class tT_Card_Ico_Combust(Card):
    CARD_KEY="T_Card_Ico_Combust"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_Combust_effect1)

class tT_Card_Ico_Combust_effect1(Effect):
    effType = EFF_TYPE.optionalInstant

    observeSignals = (LOCATION.spellTrapZone, [Signal.InBattle])

    AI_HINT = [AI_HINT.eraser]
    AI_POWER = 1

    enemy = 0
    def y_cost(self, justCheck:bool, signal):
        if not (isSignal(signal, Signal.InBattle) and signal.attackerCard.side in self.getEnemySideTuple()):
            return
        myMon = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self)
        if not myMon:
            return
        if justCheck:
            return True
        self.enemy = yield self.y_select1EnemySide()
        target = yield self.y_select1Card(myMon, TITLE.destroy, canCancel=True)
        if target:
            self.saveTarget1(target)
            return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        target = self.getLegalTarget1()
        if target:
            yield self.y_destroyCard(target)
        yield self.y_damagePlayer(self.enemy, 800)
