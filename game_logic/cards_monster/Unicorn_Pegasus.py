# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Unicorn Pegasus
卡名:独角兽珀加索斯
效果:1A:把场上1只其他怪兽返回持有者手牌。发动此效果的回合,此卡不能攻击。
"""

class Unicorn_Pegasus(Card):
    CARD_KEY = 'Unicorn_Pegasus'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Unicorn_Pegasus_e1)


class Unicorn_Pegasus_e1(Effect):
    # 1A:把场上1只其他怪兽返回持有者手牌。发动此效果的回合,此卡不能攻击。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        def isOther(c):
            return c != self.owner
        targets = self.searchCards(LOCATION.monsterZone, -1, CARD_TYPE.monster, self, isOther)
        if not targets:
            return False
        if justCheck:
            return True
        t = yield self.y_select1Card(targets, TITLE.returnToHand, canCancel=True)
        if not t:
            return False
        self.saveTarget1(t)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1()
        if not t:
            return False
        yield self.y_returnCardToHand(t)
        if self.owner.isMonsterOnField():
            yield self.y_changeCardData(self.owner, newAttackTimes=0, effDuration=EFF_DURATION.utilTurnEnds)
        return True

