# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Spotted Lynx
卡名:斑斑猞猁
效果:1A:确认对方场上1张覆盖的魔法·陷阱卡。
"""

class Lynx_LOD0(Card):
    CARD_KEY = 'Lynx_LOD0'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Lynx_LOD0_e1)


class Lynx_LOD0_e1(Effect):
    # 1A:确认对方场上1张覆盖的魔法·陷阱卡。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.search]
    EFF_POWER = 1

    def y_cost(self, justCheck, signal):
        def isSet(c):
            return c.form & FORM.set != 0
        sets = self.searchCards(LOCATION.spellTrapZone, self.getEnemySideTuple(), CARD_TYPE.all, None, isSet)
        if not sets:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        def isSet(c):
            return c.form & FORM.set != 0
        sets = self.searchCards(LOCATION.spellTrapZone, self.getEnemySideTuple(), CARD_TYPE.all, None, isSet)
        if not sets:
            return False
        # 选择=向控制者展示该盖卡(确认)
        yield self.y_select1Card(sets, TITLE.target, self.getSide(), canCancel=True)
        return True

