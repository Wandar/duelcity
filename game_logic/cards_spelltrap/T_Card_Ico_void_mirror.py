# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_void_mirror  【魔法】
卡图:粉紫背景,发光矩形镜子被黄色粗箭头斜向刺穿,虚空镜像穿透。
效果(AOTIP):
1A:以自己场上1只怪兽和对方场上1只怪兽为对象,这个回合自己的怪兽{ATK}/{DEF}变为与对方怪兽相同,
   且那只对方怪兽的效果无效化。
"""

class tT_Card_Ico_void_mirror(Card):
    CARD_KEY = "T_Card_Ico_void_mirror"
    AUTHOR = "Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_void_mirror_eff)

class tT_Card_Ico_void_mirror_eff(Effect):
    effType = EFF_TYPE.active
    activateLocation = LOCATION.spellTrapZone
    AI_HINT = [AI_HINT.enhance, AI_HINT.eraser]
    EFF_POWER = 3

    def y_cost(self, justCheck: bool, signal):
        myMons = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self)
        enMons = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self)
        if not myMons or not enMons: return False
        if justCheck: return True
        mine = yield self.y_select1Card(myMons, TITLE.target, self.getSide(), canCancel=True)
        if not mine: return False
        foe = yield self.y_select1Card(enMons, TITLE.target, self.getSide(), canCancel=True)
        if not foe: return False
        self.saveTarget1(mine)
        self.saveTarget2(foe)
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck: return True
        mine = self.getLegalTarget1()
        foe = self.getLegalTarget2()
        if mine and foe and mine.isMonsterOnField() and foe.isMonsterOnField():
            yield self.y_changeCardData(mine, newAtk=foe.atk, newDefence=foe.defence,
                                        effDuration=EFF_DURATION.utilTurnEnds, uniqueSourceID=self.effUniID)
            yield self.y_silenceCard(foe, EFF_DURATION.utilTurnEnds, self.effUniID)
        return True
