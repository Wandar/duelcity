# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Mechabeast Pterosaur
卡名:百兽机 翼龙
效果:1T:<召唤时>:从卡组把1只"百兽机"怪兽加入手牌。
"""

class SciFi_Beast03_Skin1(Card):
    CARD_KEY = 'SciFi Beast03 Skin1'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(SciFi_Beast03_Skin1_e1)


class SciFi_Beast03_Skin1_e1(Effect):
    # 1T:<召唤时>:从卡组把1只"百兽机"怪兽加入手牌。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.searchMonster]
    EFF_POWER = 3
    FAMILY = ("SciFi Beast03 Skin1", "SciFi Beast04 WhaleSnake Skin1", "SciFi Beast05_Skin1",
              "SciFi Beast06 Bull Skin2", "Sci-Fi Dragon Skin4")

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        def isFamily(c):
            return c.cardKey in self.FAMILY
        targets = self.searchCards(LOCATION.deck, self.getSide(), CARD_TYPE.monster, self, isFamily)
        if not targets:
            return False
        if justCheck:
            return True
        chosen = yield self.y_select1Card(targets, TITLE.addToHand, canCancel=True)
        if not chosen:
            return False
        self.saveTarget1(chosen)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1()
        if not t:
            return False
        yield self.y_returnCardToHand(t)
        return True

