# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Mechanical Squid
卡名:机器鱿鱼
效果:1T:<召唤时>:发现一张等级4以下的水族怪兽并特殊召唤,然后把对方场上攻击力最高的1只怪兽变为守备表示。
"""

class SKM_squid(Card):
    CARD_KEY = 'SKM_squid'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(SKM_squid_e1)


class SKM_squid_e1(Effect):
    # 1T:<召唤时>:发现一张等级4以下的水族怪兽并特殊召唤,然后把对方场上攻击力最高的1只怪兽变为守备表示。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.summoner, AI_HINT.debuff]
    EFF_POWER = 4

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        if self.freeMonsterSpace() > 0:
            picked = yield self.y_discoverCard(side=self.getSide(), race=RACE.AQUA,
                                               cardType=CARD_TYPE.monster, maxLevel=4, count=3, canCancel=True)
            if picked and self.freeMonsterSpace() > 0:
                yield self.y_specialSummon(picked)
        # 然后把对方场上攻击力最高的1只怪兽变为守备表示
        def isAtk(c):
            return c.isFaceUp() and c.form == FORM.attack
        enemies = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self, isAtk)
        if enemies:
            maxAtk = max(c.atk for c in enemies)
            target = next(c for c in enemies if c.atk == maxAtk)
            yield self.y_changeForm(target, FORM.defence)
        return True
