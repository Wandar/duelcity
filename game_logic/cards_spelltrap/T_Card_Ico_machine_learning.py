# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_machine_learning  【永续魔法】
卡图:紫橙放射光,多边形黑色大脑轮廓,内部黄色神经网络节点,机器学习/AI。
效果(AOTIP):
1T:<自己准备阶段>:只要此卡在魔陷区,自己场上所有怪兽的{ATK}永久+200(战场持续学习强化)。
"""

class tT_Card_Ico_machine_learning(Card):
    CARD_KEY = "T_Card_Ico_machine_learning"
    AUTHOR = "Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_machine_learning_eff)

class tT_Card_Ico_machine_learning_eff(Effect):
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.spellTrapZone, [Signal.StandbyPhase])
    AI_HINT = [AI_HINT.addAtk]
    EFF_POWER = 2

    def y_cost(self, justCheck: bool, signal):
        if not isSignal(signal, Signal.StandbyPhase): return False
        if self.game.whoseTurn != self.getSide(): return False
        if not self.owner.isInSpellZone(): return False
        myMons = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self)
        if not myMons: return False
        if justCheck: return True
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck: return True
        myMons = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self)
        if myMons:
            yield self.y_addCardData(myMons, attackAdd=200)
        return True
