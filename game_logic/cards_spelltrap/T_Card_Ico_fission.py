# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_fission
卡名:分裂繁殖
"""

#########################my

"""
1A:[Cost:解放自己场上1只怪兽]:特殊召唤2只该怪兽原本{ATK}一半的衍生物代币
"""

class tT_Card_Ico_fission(Card):
    CARD_KEY="T_Card_Ico_fission"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_fission_effect1)

class tT_Card_Ico_fission_effect1(Effect):
    effType = EFF_TYPE.active


    AI_HINT = [AI_HINT.summoner]
    AI_POWER = 1

    def y_cost(self, justCheck:bool, signal):
        myMon = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self)
        if not myMon:
            return
        if self.freeMonsterSpace() < 2:
            return
        if justCheck:
            return True
        target = yield self.y_select1Card(myMon, TITLE.tribute, canCancel=True)
        if target:
            self.saveTarget1(target)
            return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        target = self.getLegalTarget1()
        if not target:
            return
        halfAtk = max(0, target.atk_0 // 2)
        srcRace = target.race
        yield self.y_tributeCard(target)
        # pseudo: create 2 token monsters with halfAtk/0 and original race
        for _ in range(2):
            yield self.y_createTokenMonster(self.getSide(), atk=halfAtk, defence=0, race=srcRace, form=FORM.attack)
