# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Cloudhoof
卡名:云云麟角
效果:1P:只要此卡在场上,所有怪兽都不会被战斗破坏。
"""

class cartoonKirin(Card):
    CARD_KEY = 'cartoonKirin'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(cartoonKirin_e1)


class cartoonKirin_e1(Effect):
    # 1P:只要此卡在场上,所有怪兽都不会被战斗破坏。
    # NOTE: 引擎暂无"战斗不被破坏"的全局钩子,登记为常驻标记效果,
    #       待战斗结算时查询场上是否存在本效果以跳过战斗破坏。
    effType = EFF_TYPE.permanent
    observeSignals = (LOCATION.monsterZone, [Signal.AttachMonsterZone, Signal.DetachMonsterZone])
    AI_HINT = [AI_HINT.permanent]
    EFF_POWER = 4

    def y_signal(self, signal):
        return
        yield

