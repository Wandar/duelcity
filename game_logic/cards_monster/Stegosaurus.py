# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Stegosaurus
卡名:剑龙
效果:1T:<每个回合的结束阶段>:对方场上所有怪兽攻击力下降200。
"""

class Stegosaurus(Card):
    CARD_KEY = "Stegosaurus"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Stegosaurus_e1)


class Stegosaurus_e1(Effect):
    # 1T:<每个回合的结束阶段>:对方场上所有怪兽攻击力下降200。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.TurnEnds])
    AI_HINT = [AI_HINT.debuff]
    EFF_POWER = 2
    countLimit = COUNT_LIMIT.unlimited

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.TurnEnds):
            return False
        if not self.owner.isMonsterOnField():
            return False
        enemies = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(),
                                   CARD_TYPE.monster, self)
        if not enemies:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        enemies = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(),
                                   CARD_TYPE.monster, self)
        if enemies:
            yield self.y_addCardData(enemies, attackAdd=-200, effDuration=EFF_DURATION.onceForever)
        return True
