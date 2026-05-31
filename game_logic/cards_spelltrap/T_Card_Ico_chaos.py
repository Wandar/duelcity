# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_chaos
卡名:混沌
"""

#########################my

"""
1A:双方场上所有怪兽的表示形式互相变更,然后双方各自从卡组抽1张
"""

class tT_Card_Ico_chaos(Card):
    CARD_KEY="T_Card_Ico_chaos"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_chaos_effect1)

class tT_Card_Ico_chaos_effect1(Effect):
    effType = EFF_TYPE.active


    AI_HINT = [AI_HINT.drawCard]
    AI_POWER = 1

    enemy = 0
    def y_cost(self, justCheck:bool, signal):
        allMon = self.searchCards(LOCATION.monsterZone, -1, CARD_TYPE.monster, self)
        if not allMon:
            return
        if justCheck:
            return True
        self.enemy = yield self.y_select1EnemySide()
        return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        allMon = self.searchCards(LOCATION.monsterZone, -1, CARD_TYPE.monster, self)
        for m in allMon:
            # pseudo: flip each monster's form to the opposite
            newForm = FORM.defence if m.form == FORM.attack else FORM.attack
            yield self.y_changeForm(m, newForm)
        for side in (self.getSide(), self.enemy):
            if self.getDeckLeftNum(side):
                yield self.y_drawCard(side, 1)
