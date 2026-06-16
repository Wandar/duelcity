# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Vivid Green Dragon
卡名:苍翠龙
效果:1T:<此卡战斗破坏对方怪兽后>:发现1张等级4以下的植物族怪兽卡,把它特殊召唤。
"""

class forestdragon(Card):
    CARD_KEY = 'forestdragon'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(forestdragon_e1)


class forestdragon_e1(Effect):
    # 1T:<此卡战斗破坏对方怪兽后>:发现1张等级4以下的植物族怪兽卡,把它特殊召唤。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.BattleFinish])
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 4

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.BattleFinish):
            return False
        if signal.attackerCard != self.owner:
            return False
        rc = signal.receiverCard
        if rc is None or rc.isMonsterOnField():
            return False
        if self.freeMonsterSpace() == 0:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        picked = yield self.y_discoverCard(side=self.getSide(), race=RACE.PLANT,
                                           cardType=CARD_TYPE.monster, maxLevel=4, count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked)
        return True

