# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Druid20  【永续魔法】
卡图:绿色光芒背景,树干质感的德鲁伊张臂站立,头顶鹿角树枝,胸前螺旋图腾。
效果(AOTIP):
1T:<自己准备阶段>:只要此卡在魔陷区,自己场上所有怪兽{ATK}+100,并回复200基本分(生长光环)。
"""

class tT_Druid20(Card):
    CARD_KEY = "T_Druid20"
    AUTHOR = "Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Druid20_eff)

class tT_Druid20_eff(Effect):
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.spellTrapZone, [Signal.StandbyPhase])
    AI_HINT = [AI_HINT.addAtk, AI_HINT.recoverLP]
    EFF_POWER = 2

    def y_cost(self, justCheck: bool, signal):
        if not isSignal(signal, Signal.StandbyPhase): return False
        if self.game.whoseTurn != self.getSide(): return False
        if not self.owner.isInSpellZone(): return False
        if justCheck: return True
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck: return True
        myMons = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self)
        if myMons:
            yield self.y_addCardData(myMons, attackAdd=100)
        yield self.y_healPlayer(self.getSide(), 200)
        return True
