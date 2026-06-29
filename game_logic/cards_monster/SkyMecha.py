# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Celestial Guardian Automaton
卡名:天穹守护者
效果:1T:<召唤时>:破坏对方场上最多2张魔法·陷阱卡。2A:[把1只机械族怪兽解放]:破坏对方场上1只怪兽。
"""

class SkyMecha(Card):
    CARD_KEY = 'SkyMecha'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(SkyMecha_e1)
        self.initEffect(SkyMecha_e2)


class SkyMecha_e1(Effect):
    # 1T:<召唤时>:破坏对方场上最多2张魔法·陷阱卡。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.spellDestroyer]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        enemyST = self.searchCards(LOCATION.spellTrapZone, self.getEnemySideTuple(), CARD_TYPE.all, self)
        if not enemyST:
            return False
        if justCheck:
            return True
        maxNum = min(2, len(enemyST))
        chosen = yield self.y_selectCards(enemyST, TITLE.destroy, self.getSide(), 1, maxNum, None, True)
        if not chosen:
            return False
        self.saveTarget1(chosen)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        targets = self._getLegalTargetList1()
        if not targets:
            return False
        yield self.y_destroyCard(list(targets))
        return True


class SkyMecha_e2(Effect):
    # 2A:[把1只机械族怪兽解放]:破坏对方场上1只怪兽。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.eraser, AI_HINT.costMonster]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        def isMachine(c):
            return c.race == RACE.MACHINE
        fodder = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self, isMachine)
        if not fodder:
            return False
        enemies = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self)
        if not enemies:
            return False
        if justCheck:
            return True
        cost = yield self.y_select1Card(fodder, TITLE.tribute, canCancel=True)
        if not cost:
            return False
        target = yield self.y_select1Card(enemies, TITLE.destroy, canCancel=True)
        if not target:
            return False
        successNum = yield self.y_tributeCard(cost)
        if not successNum:
            return False
        self.saveTarget1(target)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1()
        if not t:
            return False
        yield self.y_destroyCard(t)
        return True
