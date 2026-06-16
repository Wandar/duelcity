# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Golden Flame Magma Dragon
卡名:金焰熔岩龙
效果:1T:<召唤·特殊召唤时>:对对方场上每只怪兽造成500点伤害,本回合它们不能改变表示形式。
"""

class Mdl_Monster000_0000(Card):
    CARD_KEY = 'Mdl_Monster000_0000'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Mdl_Monster000_0000_e1)


class Mdl_Monster000_0000_e1(Effect):
    # 1T:<召唤·特殊召唤时>:对对方场上每只怪兽造成500点伤害,本回合它们不能改变表示形式。
    # NOTE: "本回合不能改变表示形式" 暂无钩子,已实现全体500伤害部分。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.damager]
    EFF_POWER = 5

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        enemies = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self)
        if not enemies:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        enemies = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self)
        if enemies:
            yield self.y_damageCard(enemies, 500)
        return True

