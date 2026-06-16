# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Three-tailed Snow Wolf
卡名:三尾雪狼
效果:1T:<战斗破坏对方怪兽时>:从卡组把1只等级2以下的水属性兽族怪兽以守备表示特殊召唤。
"""

class ThreeTailedWolf(Card):
    CARD_KEY = 'ThreeTailedWolf'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(ThreeTailedWolf_e1)


class ThreeTailedWolf_e1(Effect):
    # 1T:<战斗破坏对方怪兽时>:从卡组把1只等级2以下的水属性兽族以守备表示特殊召唤。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.BattleFinish])
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.BattleFinish):
            return False
        if signal.attackerCard != self.owner:
            return False
        rc = signal.receiverCard
        if rc is None or rc.isMonsterOnField():
            return False
        def isT(c):
            return c.attr == ATTR.WATER and c.race == RACE.BEAST and c.level <= 2
        targets = self.searchCards(LOCATION.deck, self.getSide(), CARD_TYPE.monster, self, isT)
        if not targets:
            return False
        if self.freeMonsterSpace() == 0:
            return False
        if justCheck:
            return True
        chosen = yield self.y_select1Card(targets, TITLE.specialSummon, canCancel=True)
        if not chosen:
            return False
        self.saveTarget1(chosen)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1(checkLocationChange=False)
        if not t:
            return False
        yield self.y_specialSummon(t, form=FORM.defence)
        return True

