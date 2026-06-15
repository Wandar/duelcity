# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_Demon_Form  【魔法】
卡图:紫底,长角展翼的红色恶魔立于橙黄火焰光晕,霸气魔威。
效果(AOTIP):
1A:[支付1000]:以自己场上1只怪兽为对象,赋予恶魔形态——这个回合中该怪兽的{ATK}+1500。
"""

class tT_Card_Ico_Demon_Form(Card):
    CARD_KEY = "T_Card_Ico_Demon_Form"
    AUTHOR = "Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_Demon_Form_eff)

class tT_Card_Ico_Demon_Form_eff(Effect):
    effType = EFF_TYPE.active
    activateLocation = LOCATION.spellTrapZone
    AI_HINT = [AI_HINT.addAtk]
    EFF_POWER = 2

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
            yield self.y_addCardData(t, attackAdd=1500,
                                     effDuration=EFF_DURATION.utilTurnEnds,
                                     uniqueSourceID=self.effUniID)
        return True
