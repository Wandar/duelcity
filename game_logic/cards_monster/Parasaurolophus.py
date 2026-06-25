# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Parasaurolophus
卡名:副栉龙
"""

class Parasaurolophus(Card):
    CARD_KEY = "Parasaurolophus"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Parasaurolophus_EchoingRecall)


"""
1A:<战斗效果>:这张卡战斗破坏对方场上1只怪兽并将送其进墓地时，可以把那张卡放回对方卡组最上面。
1OT: <Battle effect>: When this card destroys a monster your opponent controls by battle and sends it to the Graveyard, you can return that card to the top of your opponent's Deck.
"""
class Parasaurolophus_EchoingRecall(Effect):
    effType = EFF_TYPE.optionalTrigger

    observeSignals = (LOCATION.monsterZone, [Signal.BattleFinish])

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 2

    def y_cost(self, justCheck: bool, signal: Signal.BattleFinish):
        if not isSignal(signal, Signal.BattleFinish):
            return False
        if signal.attackerCard != self.owner:
            return False

        target = signal.receiverCard
        if target is None:
            return False
        if target.side_0 not in self.getEnemySideTuple():
            return False
        # 已被战斗破坏送去墓地
        if target.isMonsterOnField():
            return False
        if target.location != LOCATION.grave:
            return False

        if justCheck:
            return True

        self.saveTarget1(target)
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck:
            return True

        target = self.getLegalTarget1(checkLocationChange=False)
        if not target:
            return False

        yield self.y_returnCardToDeck(target, returnType=RETURN_TO_DECK.top)
        return True
