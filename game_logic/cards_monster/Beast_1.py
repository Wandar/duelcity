# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Thornshell
卡名:刺壳巨兽
效果:1A:[把此卡解放]:破坏对方场上1张魔法·陷阱卡,自己抽1张卡。
"""

class Beast_1(Card):
    CARD_KEY = 'Beast_1'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Beast_1_e1)


class Beast_1_e1(Effect):
    # 1A:[把此卡解放]:破坏对方场上1张魔法·陷阱卡,自己抽1张卡。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.spellDestroyer, AI_HINT.drawCard]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        enemyST = self.searchCards(LOCATION.spellTrapZone, self.getEnemySideTuple(), CARD_TYPE.all, self)
        if not enemyST:
            return False
        if justCheck:
            return True
        t = yield self.y_select1Card(enemyST, TITLE.destroy, canCancel=True)
        if not t:
            return False
        successNum = yield self.y_tributeCard(self.owner)
        if not successNum:
            return False
        self.saveTarget1(t)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1()
        if t:
            yield self.y_destroyCard(t)
        if len(self.game.decks[self.getSide()]) > 0:
            yield self.y_drawCard(self.getSide(), 1)
        return True

