# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Dark Dragonling
卡名:黑龙宝宝
效果:1T:<我方准备阶段>:发现一张等级5以下的龙族怪兽并特殊召唤。2P:对方怪兽的攻击力不会上升。
注:2P「对方怪兽攻击力不会上升」需由 buff/数值系统在提升攻击力时读取该限制;本引擎暂无对应原语,此处仅实现 1P。
"""

class Tiger_Drago_Simple_Baby(Card):
    CARD_KEY = 'Tiger Drago Simple Baby'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Tiger_Drago_Simple_Baby_e1)


class Tiger_Drago_Simple_Baby_e1(Effect):
    # 1T:<我方准备阶段>:发现一张等级5以下的龙族怪兽并特殊召唤。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.StandbyPhase])
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 4
    countLimit = COUNT_LIMIT.unlimited

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.StandbyPhase):
            return False
        if self.game.whoseTurn != self.getSide():
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
        picked = yield self.y_discoverCard(side=self.getSide(), race=RACE.DRAGON,
                                           cardType=CARD_TYPE.monster, maxLevel=5, count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked)
        return True
