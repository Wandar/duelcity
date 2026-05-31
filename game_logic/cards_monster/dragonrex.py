# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Tyrant Dragon Rex
卡名:暴君龙王
"""

class dragonrex(Card):
    CARD_KEY = "dragonrex"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(dragonrex_RexCataclysm)



"""
1A:<场上效果>[丢弃一张魔法·陷阱卡]:破坏对方场上的1张魔法·陷阱卡。
1A:<Field effect>[Discard 1 Spell/Trap]: Destroy 1 Spell/Trap on your opponent's field.
"""
class dragonrex_RexCataclysm(Effect):
    effType = EFF_TYPE.active

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 3

    def y_cost(self, justCheck: bool, signal):
        if not self.owner.isMonsterOnField():
            return False

        def isSpellTrap(c):
            return c.type in (CARD_TYPE.spell, CARD_TYPE.trap)

        handST = self.searchCards(LOCATION.hand, self.getSide(), CARD_TYPE.all, self, isSpellTrap)
        if not handST:
            return False

        enemyST = self.searchCards(
            LOCATION.spellTrapZone, self.getEnemySideTuple(), CARD_TYPE.all, None, isSpellTrap
        )
        if not enemyST:
            return False

        if justCheck:
            return True

        chosenDiscard = yield self.y_select1Card(handST, TITLE.sendToGrave, canCancel=True)
        if not chosenDiscard:
            return False
        chosenTarget = yield self.y_select1Card(enemyST, TITLE.destroy, canCancel=True)
        if not chosenTarget:
            return False

        yield self.y_sendCardToGrave(chosenDiscard)
        self.saveTarget1(chosenTarget)
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck:
            return True
        target = self.getLegalTarget1(checkLocationChange=True)
        if not target:
            return False
        yield self.y_destroyCard(target)
        return True
