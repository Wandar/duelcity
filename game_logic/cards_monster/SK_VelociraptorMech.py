# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Mechanical Velociraptor
卡名:机器速龙
效果:1T:<战斗破坏对方怪兽时>:从卡组把1只等级4以下的机械族怪兽加入手牌。
"""

class SK_VelociraptorMech(Card):
    CARD_KEY = 'SK_VelociraptorMech'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(SK_VelociraptorMech_e1)


class SK_VelociraptorMech_e1(Effect):
    # 1T:<战斗破坏对方怪兽时>:从卡组把1只等级4以下的机械族怪兽加入手牌。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.BattleFinish])
    AI_HINT = [AI_HINT.searchMonster]
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
            return c.race == RACE.MACHINE and c.level <= 4
        targets = self.searchCards(LOCATION.deck, self.getSide(), CARD_TYPE.monster, self, isT)
        if not targets:
            return False
        if justCheck:
            return True
        chosen = yield self.y_select1Card(targets, TITLE.addToHand, canCancel=True)
        if not chosen:
            return False
        self.saveTarget1(chosen)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1()
        if not t:
            return False
        yield self.y_returnCardToHand(t)
        return True

