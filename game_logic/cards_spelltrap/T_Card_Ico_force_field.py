# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_force_field  【陷阱】
卡图:蓝紫背景,多道蓝白光束汇聚击打青色球体,力场防护。
效果(AOTIP):
1OT:<对方怪兽宣告攻击时>:展开力场——这个回合中,自己场上的怪兽不会被战斗破坏(不受战斗伤害)。
"""

class tT_Card_Ico_force_field(Card):
    CARD_KEY = "T_Card_Ico_force_field"
    AUTHOR = "Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_force_field_eff)

class tT_Card_Ico_force_field_eff(Effect):
    effType = EFF_TYPE.optionalTrigger
    observeSignals = (LOCATION.spellTrapZone, [Signal.RequestBattle])
    AI_HINT = [AI_HINT.enhance]
    EFF_POWER = 3

    def y_cost(self, justCheck: bool, signal):
        if not isSignal(signal, Signal.RequestBattle): return False
        atkCard = signal.attackerCard
        if atkCard is None or atkCard.side not in self.getEnemySideTuple(): return False
        myMons = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self)
        if not myMons: return False
        if justCheck: return True
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck: return True
        myMons = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self)
        if myMons:
            yield self.y_addImmunityBuffToCard(myMons, IMMUNITY_MASK.battleDamage,
                                               EFF_DURATION.utilTurnEnds, self.effUniID)
        return True
