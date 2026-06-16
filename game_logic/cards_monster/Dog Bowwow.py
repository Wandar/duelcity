# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Blastfire Hound
卡名:爆火狂犬
效果:1P:此卡攻击的回合,对方不能发动魔法卡。
"""

class Dog_Bowwow(Card):
    CARD_KEY = 'Dog Bowwow'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Dog_Bowwow_e1)


class Dog_Bowwow_e1(Effect):
    # 1P:此卡攻击的回合,对方不能发动魔法卡。
    # NOTE: 引擎暂无"禁止发动魔法"的玩家钩子,登记为常驻标记效果(战斗时记录),待引擎支持。
    effType = EFF_TYPE.permanent
    observeSignals = (LOCATION.monsterZone, [Signal.AttachMonsterZone, Signal.DetachMonsterZone])
    AI_HINT = [AI_HINT.permanent]
    EFF_POWER = 2

    def y_signal(self, signal):
        return
        yield

