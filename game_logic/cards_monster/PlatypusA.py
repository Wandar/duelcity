# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Waterside PlatypusA
卡名:水缘鸭嘴兽
效果:1P:此卡同时当作兽族·水族·鸟兽族使用。
"""

class PlatypusA(Card):
    CARD_KEY = 'PlatypusA'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(PlatypusA_e1)


class PlatypusA_e1(Effect):
    # 1P:此卡同时当作兽族·水族·鸟兽族使用。
    # NOTE: 引擎种族字段为单值,暂不支持多种族并存,登记为常驻标记效果,待引擎支持种族掩码。
    effType = EFF_TYPE.permanent
    observeSignals = (LOCATION.monsterZone, [Signal.AttachMonsterZone, Signal.DetachMonsterZone])
    AI_HINT = [AI_HINT.permanent]
    EFF_POWER = 1

    def y_signal(self, signal):
        return
        yield

