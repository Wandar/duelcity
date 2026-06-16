# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Vineplate Forest Guard
卡名:藤甲守林卫
效果:1P:自己其他植物族·龙族怪兽不会被对方的卡的效果破坏。
"""

class TreantGuard_Green(Card):
    CARD_KEY = 'TreantGuard-Green'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(TreantGuard_Green_e1)


class TreantGuard_Green_e1(Effect):
    # 1P:自己其他植物族·龙族怪兽不会被对方的卡的效果破坏。
    # NOTE: 引擎暂无"效果破坏保护"的查询钩子,登记为常驻标记效果,待破坏流程查询。
    effType = EFF_TYPE.permanent
    observeSignals = (LOCATION.monsterZone, [Signal.AttachMonsterZone, Signal.DetachMonsterZone])
    AI_HINT = [AI_HINT.permanent]
    EFF_POWER = 4

    def y_signal(self, signal):
        return
        yield

