# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Emerald Crystal Lizard
卡名:碧空晶蜥
效果:1P:此卡不会被战斗破坏,且攻击守备表示怪兽时给予贯通伤害。
"""

class Wyrm1_2(Card):
    CARD_KEY = 'Wyrm1_2'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Wyrm1_2_e1)


class Wyrm1_2_e1(Effect):
    # 1P:此卡不会被战斗破坏,且攻击守备表示怪兽时给予贯通伤害。
    # NOTE: "战斗不被破坏" 与 "贯通" 暂无钩子,登记为常驻标记效果,待战斗结算查询。
    effType = EFF_TYPE.permanent
    observeSignals = (LOCATION.monsterZone, [Signal.AttachMonsterZone, Signal.DetachMonsterZone])
    AI_HINT = [AI_HINT.permanent, AI_HINT.battleBenefit]
    EFF_POWER = 4

    def y_signal(self, signal):
        return
        yield

