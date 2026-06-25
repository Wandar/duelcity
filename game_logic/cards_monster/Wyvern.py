# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Tyrant Dragon
卡名:暴君龙
effect:
效果:1T:<召唤时>:破坏对方场上攻击力最高的1只怪兽。
"""

class Wyvern(Card):
    CARD_KEY = "Wyvern"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Wyvern_e1)


class Wyvern_e1(Effect):
    # 1T:<召唤时>:破坏对方场上攻击力最高的1只怪兽。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 4

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        enemies = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(),
                                   CARD_TYPE.monster, self)
        if not enemies:
            return False
        if justCheck:
            return True

        maxAtk = max(c.atk for c in enemies)
        tops = [c for c in enemies if c.atk == maxAtk]
        if len(tops) == 1:
            chosen = tops[0]
        else:
            chosen = yield self.y_select1Card(tops, TITLE.destroy, canCancel=False)
        if not chosen:
            return False
        self.saveTarget1(chosen)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        target = self.getLegalTarget1()
        if not target:
            return False
        yield self.y_destroyCard(target)
        return True
