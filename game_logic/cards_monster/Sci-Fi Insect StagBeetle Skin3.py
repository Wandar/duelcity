# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Mecha Stag Beetle
卡名:机械锹形虫
效果:1A:[把此卡解放]:破坏对方场上攻击力最高的怪兽。
"""

class Sci_Fi_Insect_StagBeetle_Skin3(Card):
    CARD_KEY = 'Sci-Fi Insect StagBeetle Skin3'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Sci_Fi_Insect_StagBeetle_Skin3_e1)


class Sci_Fi_Insect_StagBeetle_Skin3_e1(Effect):
    # 1A:[把此卡解放]:破坏对方场上攻击力最高的怪兽。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 4

    def y_cost(self, justCheck, signal):
        enemies = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self)
        if not enemies:
            return False
        if justCheck:
            return True
        successNum = yield self.y_tributeCard(self.owner)
        if not successNum:
            return False
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        enemies = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self)
        if not enemies:
            return False
        best = max(enemies, key=lambda c: c.atk)
        yield self.y_destroyCard(best)
        return True

