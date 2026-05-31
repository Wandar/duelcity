# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Tyrant Dragon
卡名:暴君龙
"""

class Wyvern(Card):
    CARD_KEY = "Wyvern"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Wyvern_TyrantMenace)


"""
1I:<场上效果>:对手特殊召唤怪兽时,若该怪兽的攻击力低于此卡，直接将其破坏；否则该怪兽{ATK}-1000{UTIL}。
1I: <When your opponent Special Summons a monster>: If that monster's ATK is lower than this card's ATK, destroy it immediately; otherwise, that monster loses 1000 ATK until the end of this turn.
"""
class Wyvern_TyrantMenace(Effect):
    effType = EFF_TYPE.instant

    observeSignals = (LOCATION.monsterZone, [Signal.SpecialSummon])

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 4

    def y_activate(self, justCheck: bool, signal: Signal.SpecialSummon):
        if not (isSignal(signal, Signal.SpecialSummon)
                and signal.card.side in self.getEnemySideTuple()):
            return False
        if not signal.card.isMonsterOnField():
            return False
        if not self.owner.isMonsterOnField():
            return False

        if justCheck:
            return True

        target = signal.card
        if target.atk < self.owner.atk:
            yield self.y_destroyCard(target)
        else:
            yield self.y_addCardData(target, attackAdd=-1000, effDuration=EFF_DURATION.utilTurnEnds)
        return True
