# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_Combust  【魔法】
卡图:橙红火焰爆炸,人形剪影立于黄白光芒中央,四周巨型火球与火焰云环绕。
效果(AOTIP):
1A:[解放自己场上1只怪兽]:令其引爆成新星——对对方造成该怪兽{ATK}的伤害,
   并对场上其他所有怪兽造成该怪兽{ATK}一半的伤害。
"""

class tT_Card_Ico_Combust(Card):
    CARD_KEY = "T_Card_Ico_Combust"
    AUTHOR = "Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_Combust_eff)

class tT_Card_Ico_Combust_eff(Effect):
    effType = EFF_TYPE.active
    activateLocation = LOCATION.spellTrapZone
    AI_HINT = [AI_HINT.damager, AI_HINT.eraser]
    EFF_POWER = 4
    blastAtk = 0

    def y_cost(self, justCheck: bool, signal):
        myMons = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self)
        if not myMons: return False
        if justCheck: return True
        fuel = yield self.y_select1Card(myMons, TITLE.tribute, self.getSide(), canCancel=True)
        if not fuel: return False
        self.blastAtk = fuel.atk
        successNum = yield self.y_tributeCard(fuel)
        if not successNum: return False
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck: return True
        blast = self.blastAtk
        self.blastAtk = 0
        if blast > 0:
            yield self.y_damagePlayer(self.getEnemySideTuple(), blast)
        others = self.searchCards(LOCATION.monsterZone, -1, CARD_TYPE.monster, self)
        if others and blast > 0:
            yield self.y_damageCard(others, blast // 2)
        return True
