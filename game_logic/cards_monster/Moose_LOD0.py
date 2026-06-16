# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Great Antler Moose
卡名:大角驼鹿
效果:1P:对方怪兽不能选择自己场上其他兽族怪兽作为攻击对象。
"""

class Moose_LOD0(Card):
    CARD_KEY = 'Moose_LOD0'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Moose_LOD0_e1)


class Moose_LOD0_e1(Effect):
    # 1P:对方怪兽不能选择自己场上其他兽族怪兽作为攻击对象。
    # NOTE: 引擎暂无"限定攻击目标"的钩子,登记为常驻标记效果,待战斗目标选择时查询。
    effType = EFF_TYPE.permanent
    observeSignals = (LOCATION.monsterZone, [Signal.AttachMonsterZone, Signal.DetachMonsterZone])
    AI_HINT = [AI_HINT.permanent]
    EFF_POWER = 3

    def y_signal(self, signal):
        return
        yield

