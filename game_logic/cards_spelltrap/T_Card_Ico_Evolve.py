# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_Evolve
卡名:进化
"""

#########################my

"""
1A:[Cost:解放自己场上1只怪兽]:从卡组特殊召唤1只比其等级高2级的同族怪兽
"""

class tT_Card_Ico_Evolve(Card):
    CARD_KEY="T_Card_Ico_Evolve"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_Evolve_effect1)

class tT_Card_Ico_Evolve_effect1(Effect):
    effType = EFF_TYPE.active


    AI_HINT = [AI_HINT.summoner]
    AI_POWER = 1

    def y_cost(self, justCheck:bool, signal):
        myMonsters = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self)
        if not myMonsters:
            return
        if not self.getDeckLeftNum():
            return
        if justCheck:
            return True
        target = yield self.y_select1Card(myMonsters, TITLE.tribute, canCancel=True)
        if target:
            self.saveTarget1(target)
            return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        sacrifice = self.getLegalTarget1()
        if not sacrifice:
            return
        targetLv = sacrifice.level + 2
        targetRace = sacrifice.race
        yield self.y_tributeCard(sacrifice)
        def f(c):
            return c.level == targetLv and c.race == targetRace
        # pseudo: search deck for matching monster then special-summon
        deckCards = self.searchCards(LOCATION.deck, self.getSide(), CARD_TYPE.monster, self, f)
        if deckCards:
            pick = yield self.y_select1Card(deckCards, TITLE.specialSummon, canCancel=True)
            if pick:
                yield self.y_specialSummon(pick, self.getSide(), FORM.attack)
