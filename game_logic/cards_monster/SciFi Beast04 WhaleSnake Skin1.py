# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Mechabeast Whale
卡名:百兽机 黑鲸
效果:1A:[把1只"百兽机"怪兽解放]:自己抽2张卡。
"""

class SciFi_Beast04_WhaleSnake_Skin1(Card):
    CARD_KEY = 'SciFi Beast04 WhaleSnake Skin1'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(SciFi_Beast04_WhaleSnake_Skin1_e1)


class SciFi_Beast04_WhaleSnake_Skin1_e1(Effect):
    # 1A:[把1只"百兽机"怪兽解放]:自己抽2张卡。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.drawCard, AI_HINT.costMonster]
    EFF_POWER = 3
    FAMILY = ("SciFi Beast03 Skin1", "SciFi Beast04 WhaleSnake Skin1", "SciFi Beast05_Skin1",
              "SciFi Beast06 Bull Skin2", "Sci-Fi Dragon Skin4")

    def y_cost(self, justCheck, signal):
        def isFamily(c):
            return c.cardKey in self.FAMILY
        fodder = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self, isFamily)
        if not fodder:
            return False
        if len(self.game.decks[self.getSide()]) < 1:
            return False
        if justCheck:
            return True
        cost = yield self.y_select1Card(fodder, TITLE.tribute, canCancel=True)
        if not cost:
            return False
        successNum = yield self.y_tributeCard(cost)
        if not successNum:
            return False
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        n = min(2, len(self.game.decks[self.getSide()]))
        if n > 0:
            yield self.y_drawCard(self.getSide(), n)
        return True

