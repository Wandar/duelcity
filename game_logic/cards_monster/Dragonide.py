# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Hammer Lizard
卡名:铁锤蜥蜴
效果:1T:<战斗破坏对方怪兽时>:破坏对方场上1张魔法·陷阱卡。
"""

class Dragonide(Card):
    CARD_KEY = "Dragonide"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Dragonide_e1)


class Dragonide_e1(Effect):
    # 1T:<战斗破坏对方怪兽时>:破坏对方场上1张魔法·陷阱卡。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.BattleFinish])
    AI_HINT = [AI_HINT.spellDestroyer]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.BattleFinish):
            return False
        if signal.attackerCard != self.owner:
            return False
        rc = signal.receiverCard
        if rc is None or rc.isMonsterOnField():
            return False
        enemyST = self.searchCards(LOCATION.spellTrapZone, self.getEnemySideTuple(), CARD_TYPE.all, self)
        if not enemyST:
            return False
        if justCheck:
            return True
        t = yield self.y_select1Card(enemyST, TITLE.destroy, canCancel=True)
        if not t:
            return False
        self.saveTarget1(t)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1()
        if not t:
            return False
        yield self.y_destroyCard(t)
        return True
