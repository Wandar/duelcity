# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Nimble Drakonoid
卡名:灵巧机龙
效果:1T:此卡进行战斗的伤害计算后,可以把此卡变为守备表示,并自己抽1张卡。
"""

class Dragon_Bot(Card):
    CARD_KEY = 'Dragon Bot'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Dragon_Bot_e1)


class Dragon_Bot_e1(Effect):
    # 1T:此卡进行战斗的伤害计算后,可以把此卡变为守备表示,并自己抽1张卡。
    effType = EFF_TYPE.optionalTrigger
    observeSignals = (LOCATION.monsterZone, [Signal.BattleFinish])
    AI_HINT = [AI_HINT.drawCard]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.BattleFinish):
            return False
        if signal.attackerCard != self.owner and signal.receiverCard != self.owner:
            return False
        if not self.owner.isMonsterOnField():
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        yield self.y_changeForm(self.owner, FORM.defence)
        yield self.y_drawCard(self.getSide(), 1)
        return True

