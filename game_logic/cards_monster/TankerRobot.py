# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Power Steel
卡名:动力钢铁
效果:1A:[献祭此卡]:自己回复1000点。
"""

class TankerRobot(Card):
    CARD_KEY = 'TankerRobot'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(TankerRobot_e1)


class TankerRobot_e1(Effect):
    # 1A:[献祭此卡]:自己回复1000点。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.recoverLP]
    EFF_POWER = 2

    def y_cost(self, justCheck, signal):
        if not self.owner.isMonsterOnField():
            return False
        if justCheck:
            return True
        successNum = yield self.y_tributeCard(self.owner)
        if not successNum:
            return False
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        yield self.y_healPlayer(self.getSide(), 1000)
        return True

