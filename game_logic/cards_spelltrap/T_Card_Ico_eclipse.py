# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_eclipse  【魔法】
卡图:深红背景,漆黑星体遮住右侧橙黄发光太阳,形成日食。
效果(AOTIP):
1A:日食降临——直到对方下个回合结束,对方场上怪兽的{ATK}减半,且对方不能进行攻击宣言。
"""

class tT_Card_Ico_eclipse(Card):
    CARD_KEY = "T_Card_Ico_eclipse"
    AUTHOR = "Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_eclipse_eff)

class tT_Card_Ico_eclipse_eff(Effect):
    effType = EFF_TYPE.active
    activateLocation = LOCATION.spellTrapZone
    AI_HINT = [AI_HINT.debuff]
    EFF_POWER = 4

    def y_cost(self, justCheck: bool, signal):
        if justCheck: return True
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck: return True
        enMons = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self)
        if enMons:
            yield self.y_multiplyCardData(enMons, attackMulti=0.5,
                                          effDuration=EFF_DURATION.utilNextTurnEnds, sourceID=self.effUniID)
        for s in self.getEnemySideTuple():
            yield self.y_addPlayerBuff(s, PLAYER_BUFF.cantDeclareAttack,
                                       EFF_DURATION.utilNextTurnEnds, self.effUniID)
        return True
