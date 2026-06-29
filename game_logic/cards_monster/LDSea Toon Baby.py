# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Sea Dragonling
卡名:海龙宝宝
效果:1T:<召唤时>:发现一张等级5以下的龙族怪兽并特殊召唤。2T:<召唤时>:把对方场上攻击力最高的1只怪兽变为守备表示且无法变更表示形式。
"""

class LDSea_Toon_Baby(Card):
    CARD_KEY = 'LDSea Toon Baby'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(LDSea_Toon_Baby_e1)
        self.initEffect(LDSea_Toon_Baby_e2)


class LDSea_Toon_Baby_e1(Effect):
    # 1T:<召唤时>:发现一张等级5以下的龙族怪兽并特殊召唤。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 4

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        if self.freeMonsterSpace() == 0:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        picked = yield self.y_discoverCard(side=self.getSide(), race=RACE.DRAGON,
                                           cardType=CARD_TYPE.monster, maxLevel=5, count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked)
        return True


class LDSea_Toon_Baby_e2(Effect):
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
        # y_changeForm 改守备并自动锁定本回合无法变更表示形式
        yield self.y_changeForm(target, FORM.defence)
        return True
