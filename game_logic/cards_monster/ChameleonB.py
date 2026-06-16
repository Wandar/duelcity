# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Meadow Camo Chameleon Blue
卡名:树影伪装者·蓝
效果:1I:对方的效果选择自己其他怪兽为对象时,改为以此卡为对象。
"""

class ChameleonB(Card):
    CARD_KEY = 'ChameleonB'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(ChameleonB_e1)


class ChameleonB_e1(Effect):
    # 1I:对方的效果选择自己其他怪兽为对象时,改为以此卡为对象。
    # NOTE: 引擎暂无"对象替换/护身"的钩子,登记为常驻标记效果,待目标选择阶段查询。
    effType = EFF_TYPE.permanent
    observeSignals = (LOCATION.monsterZone, [Signal.AttachMonsterZone, Signal.DetachMonsterZone])
    AI_HINT = [AI_HINT.permanent]
    EFF_POWER = 2

    def y_signal(self, signal):
        return
        yield

