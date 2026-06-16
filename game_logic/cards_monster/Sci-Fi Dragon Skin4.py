# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Mechabeast ChenLoong
卡名:百兽机 辰龙
效果:1T:<召唤时>:从卡组把1只"百兽机"特殊召唤,之后可破坏对方场上1张卡。
"""

class Sci_Fi_Dragon_Skin4(Card):
    CARD_KEY = 'Sci-Fi Dragon Skin4'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Sci_Fi_Dragon_Skin4_e1)


class Sci_Fi_Dragon_Skin4_e1(Effect):
    # 1T:<召唤时>:从卡组把1只"百兽机"特殊召唤,之后可破坏对方场上1张卡。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.summoner, AI_HINT.eraser]
    EFF_POWER = 5
    FAMILY = ("SciFi Beast03 Skin1", "SciFi Beast04 WhaleSnake Skin1", "SciFi Beast05_Skin1",
              "SciFi Beast06 Bull Skin2", "Sci-Fi Dragon Skin4")

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        def isFamily(c):
            return c != self.owner and c.cardKey in self.FAMILY
        targets = self.searchCards(LOCATION.deck, self.getSide(), CARD_TYPE.monster, self, isFamily)
        if not targets:
            return False
        if self.freeMonsterSpace() == 0:
            return False
        if justCheck:
            return True
        chosen = yield self.y_select1Card(targets, TITLE.specialSummon, canCancel=True)
        if not chosen:
            return False
        self.saveTarget1(chosen)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1(checkLocationChange=False)
        if not t:
            return False
        yield self.y_specialSummon(t)
        enemies = self.searchCards(LOCATION.mask_onField, self.getEnemySideTuple(), CARD_TYPE.all, self)
        if enemies:
            chosen = yield self.y_select1Card(enemies, TITLE.destroy, self.getSide(), canCancel=True)
            if chosen:
                yield self.y_destroyCard(chosen)
        return True

