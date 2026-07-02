# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Breeze Sprite King
卡名:微风精灵王
效果:1T:<对方怪兽召唤时>:发现一张等级4以下的天使族怪兽并特殊召唤。2T:<我方准备阶段>:此卡攻击力·守备力上升500。
"""

class Wind_Mage(Card):
    CARD_KEY = 'Wind Mage'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Wind_Mage_e1)
        self.initEffect(Wind_Mage_e2)


class Wind_Mage_e1(Effect):
    # 1T:<对方怪兽召唤时>:发现一张等级4以下的天使族怪兽并特殊召唤。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 4

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon):
            return False
        scard = getattr(signal, "card", None)
        if scard is None or scard == self.owner or self.checkAlly(scard):
            return False
        if not self.owner.isMonsterOnField():
            return False
        if self.freeMonsterSpace() == 0:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        picked = yield self.y_discoverCard(title=TITLE.specialSummon, side=self.getSide(), race=RACE.FAIRY,
                                           cardType=CARD_TYPE.monster, maxLevel=4, count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked)
        return True


class Wind_Mage_e2(Effect):
    # 2T:<我方准备阶段>:此卡攻击力·守备力上升500。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.StandbyPhase])
    AI_HINT = [AI_HINT.enhance]
    EFF_POWER = 2
    countLimit = COUNT_LIMIT.unlimited

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.StandbyPhase):
            return False
        if self.game.whoseTurn != self.getSide():
            return False
        if not self.owner.isMonsterOnField():
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        yield self.y_addCardData(self.owner, attackAdd=500, defenceAdd=500, effDuration=EFF_DURATION.onceForever)
        return True
