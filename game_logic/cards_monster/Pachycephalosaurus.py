# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Pachycephalosaurus
卡名:肿头龙
效果:1T:<战斗破坏对方怪兽时>:可再破坏对方场上1张卡。
"""

class Pachycephalosaurus(Card):
    CARD_KEY = "Pachycephalosaurus"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Pachycephalosaurus_e1)


class Pachycephalosaurus_e1(Effect):
    # 1T:<战斗破坏对方怪兽时>:可再破坏对方场上1张卡。
    effType = EFF_TYPE.optionalTrigger
    observeSignals = (LOCATION.monsterZone, [Signal.BattleFinish])
    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.BattleFinish):
            return False
        if signal.attackerCard != self.owner:
            return False
        rc = signal.receiverCard
        if rc is None or rc.isMonsterOnField():
            return False
        enemyAll = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self)
        enemyST = self.searchCards(LOCATION.spellTrapZone, self.getEnemySideTuple(), CARD_TYPE.all, self)
        targets = enemyAll + enemyST
        if not targets:
            return False
        if justCheck:
            return True
        t = yield self.y_select1Card(targets, TITLE.destroy, canCancel=True)
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
