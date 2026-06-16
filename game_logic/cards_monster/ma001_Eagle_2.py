# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Gale Eagle
卡名:疾风鹰
效果:1P:此卡在召唤的回合可以直接攻击。
"""

class ma001_Eagle_2(Card):
    CARD_KEY = 'ma001_Eagle_2'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(ma001_Eagle_2_e1)


class ma001_Eagle_2_e1(Effect):
    # 1P:此卡在召唤的回合可以直接攻击。
    # NOTE: 引擎暂无"可直接攻击"的卡级钩子,登记为常驻标记效果,待战斗目标判定时查询。
    effType = EFF_TYPE.permanent
    observeSignals = (LOCATION.monsterZone, [Signal.AttachMonsterZone, Signal.DetachMonsterZone])
    AI_HINT = [AI_HINT.permanent]
    EFF_POWER = 2

    def y_signal(self, signal):
        return
        yield

