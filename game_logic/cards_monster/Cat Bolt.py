# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Red Lightning Cat
卡名:红闪电猫
效果:1T:<对方怪兽召唤时>:发现一张等级2以下的兽族怪兽并守备召唤。
"""

class Cat_Bolt(Card):
    CARD_KEY = "Cat Bolt"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Cat_Bolt_e1)


class Cat_Bolt_e1(Effect):
    # 1T:<对方怪兽召唤时>:发现一张等级2以下的兽族怪兽并守备召唤。
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
        picked = yield self.y_discoverCard(side=self.getSide(), race=RACE.BEAST,
                                           cardType=CARD_TYPE.monster, maxLevel=2, count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked, form=FORM.defence)
        return True
