# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Crystal Elemental Guardian
卡名:水晶元素守护者
效果:1T:<召唤时>:发现1张水属性怪兽卡。
"""

class CrystalElemental_Cave(Card):
    CARD_KEY = "CrystalElemental_Cave"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(CrystalElemental_Cave_e1)


class CrystalElemental_Cave_e1(Effect):
    # 1T:<召唤时>:发现1张水属性怪兽卡。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.searchMonster]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        yield self.y_discoverCard(side=self.getSide(), attr=ATTR.WATER,
                                  cardType=CARD_TYPE.monster, count=3, canCancel=True)
        return True
