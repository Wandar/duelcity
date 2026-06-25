# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Pachycephalosaurus
卡名:肿头龙
effect:
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
    EFF_POWER = 2

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.BattleFinish):
            return False
        if signal.attackerCard != self.owner:
            return False
        rc = signal.receiverCard
        if rc is None or rc.isMonsterOnField():
            return False
        targets = self.searchCards(LOCATION.mask_onField, self.getEnemySideTuple(),
                                   CARD_TYPE.all, self)
        if not targets:
            return False
        if justCheck:
            return True

        chosen = yield self.y_select1Card(targets, TITLE.destroy, canCancel=True)
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
