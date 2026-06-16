# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Pawsguard
卡名:爪爪守卫
效果:1P:只要此卡在场上,双方都不能从弃牌区特殊召唤怪兽。
"""

class cartoonCerberus(Card):
    CARD_KEY = 'cartoonCerberus'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(cartoonCerberus_e1)


class cartoonCerberus_e1(Effect):
    # 1P:只要此卡在场上,双方都不能从弃牌区特殊召唤怪兽。
    # NOTE: 引擎暂无"禁止从墓地特殊召唤"的全局钩子,这里登记为常驻标记效果,
    #       待引擎在 Card.canSummon / 特殊召唤流程中查询场上是否存在本效果时生效。
    effType = EFF_TYPE.permanent
    observeSignals = (LOCATION.monsterZone, [Signal.AttachMonsterZone, Signal.DetachMonsterZone])
    AI_HINT = [AI_HINT.permanent]
    EFF_POWER = 4

    def y_signal(self, signal):
        return
        yield

