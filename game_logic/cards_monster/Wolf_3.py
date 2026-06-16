# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Icebreak Claw
卡名:裂冰之爪
效果:1A:[把此卡解放]:破坏对方场上1只守备表示怪兽,自己抽1张卡。
"""

class Wolf_3(Card):
    CARD_KEY = 'Wolf_3'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Wolf_3_e1)


class Wolf_3_e1(Effect):
    # 1A:[把此卡解放]:破坏对方场上1只守备表示怪兽,自己抽1张卡。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.eraser, AI_HINT.drawCard]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        def isDef(c):
            return c.form in (FORM.defence, FORM.defenceSet)
        targets = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self, isDef)
        if not targets:
            return False
        if justCheck:
            return True
        t = yield self.y_select1Card(targets, TITLE.destroy, canCancel=True)
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

