# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_ball_lightning  【魔法】
卡图:紫底,黑色手掌托举红色火球,周围迸射黄色闪电,掌控闪电球。
效果(AOTIP):
1A:以对方场上1只怪兽为对象,对它造成600伤害;若它因此被破坏,闪电弹跳,
   对对方场上另1只怪兽再造成600伤害。
"""

class tT_Card_Ico_ball_lightning(Card):
    CARD_KEY = "T_Card_Ico_ball_lightning"
    AUTHOR = "Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_ball_lightning_eff)

class tT_Card_Ico_ball_lightning_eff(Effect):
    effType = EFF_TYPE.active
    activateLocation = LOCATION.spellTrapZone
    AI_HINT = [AI_HINT.damager]
    EFF_POWER = 3

    def y_cost(self, justCheck: bool, signal):
        enMons = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self)
        if not enMons: return False
        if justCheck: return True
        t = yield self.y_select1Card(enMons, TITLE.target, self.getSide(), canCancel=True)
        if not t: return False
        self.saveTarget1(t)
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck: return True
        t = self.getLegalTarget1()
        if not t: return False
        yield self.y_damageCard(t, 600)
        if not t.isMonsterOnField():
            others = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self)
            if others:
                yield self.y_damageCard(others[0], 600)
        return True
