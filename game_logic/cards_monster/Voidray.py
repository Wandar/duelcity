# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Batdrake
卡名:飞蝠龙
效果:1A:[支付800基本分]:发现一张等级4以下的水族怪兽并特殊召唤。2T:<召唤时>:把对方场上攻击力最高的1只怪兽变为守备表示且无法变更表示形式。
"""

class Voidray(Card):
    CARD_KEY = 'Voidray'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Voidray_e1)
        self.initEffect(Voidray_e2)


class Voidray_e1(Effect):
    # 1A:[支付800基本分]:发现一张等级4以下的水族怪兽并特殊召唤。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.summoner, AI_HINT.highCost]
    EFF_POWER = 4

    def y_cost(self, justCheck, signal):
        if self.game.LPs[self.getSide()] <= 800:
            return False
        if self.freeMonsterSpace() == 0:
            return False
        if justCheck:
            return True
        yield self.y_damagePlayer(self.getSide(), 800)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        if self.freeMonsterSpace() == 0:
            return False
        picked = yield self.y_discoverCard(side=self.getSide(), race=RACE.AQUA,
                                           cardType=CARD_TYPE.monster, maxLevel=4, count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked)
        return True


class Voidray_e2(Effect):
    # 2T:<召唤时>:把对方场上攻击力最高的1只怪兽变为守备表示且无法变更表示形式。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.debuff]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        def isAtk(c):
            return c.isFaceUp() and c.form == FORM.attack
        enemies = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self, isAtk)
        if not enemies:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        def isAtk(c):
            return c.isFaceUp() and c.form == FORM.attack
        enemies = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self, isAtk)
        if not enemies:
            return False
        maxAtk = max(c.atk for c in enemies)
        target = next(c for c in enemies if c.atk == maxAtk)
        yield self.y_changeForm(target, FORM.defence)
        return True
