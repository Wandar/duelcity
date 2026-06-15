# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_overclock  【魔法】
卡图:橙红火焰背景,黑色仪表盘指针指向红区,红绿渐变刻度,超频加速。
效果(AOTIP):
1A:以自己场上1只怪兽为对象,这个回合其{ATK}+2000;作为超频反噬,自己受到1000伤害。
"""

class tT_Card_Ico_overclock(Card):
    CARD_KEY = "T_Card_Ico_overclock"
    AUTHOR = "Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_overclock_eff)

class tT_Card_Ico_overclock_eff(Effect):
    effType = EFF_TYPE.active
    activateLocation = LOCATION.spellTrapZone
    AI_HINT = [AI_HINT.addAtk]
    EFF_POWER = 3

    def y_cost(self, justCheck: bool, signal):
        if self.game.LPs[self.getSide()] <= 1000: return False
        myMons = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self)
        if not myMons: return False
        if justCheck: return True
        t = yield self.y_select1Card(myMons, TITLE.target, self.getSide(), canCancel=True)
        if not t: return False
        yield self.y_damagePlayer(self.getSide(), 1000)
        self.saveTarget1(t)
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck: return True
        t = self.getLegalTarget1()
        if t and t.isMonsterOnField():
            yield self.y_addCardData(t, attackAdd=2000,
                                     effDuration=EFF_DURATION.utilTurnEnds, uniqueSourceID=self.effUniID)
        return True
