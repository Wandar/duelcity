# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Green Shade Murmurer
卡名:绿影咕哝者
效果:1A:[把此卡解放]:对对方造成1000点伤害。
"""

class SM_EnemyGoblin(Card):
    CARD_KEY = 'SM_EnemyGoblin'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(SM_EnemyGoblin_e1)


class SM_EnemyGoblin_e1(Effect):
    # 1A:[把此卡解放]:对对方造成1000点伤害。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.damager, AI_HINT.costMonster]
    EFF_POWER = 3

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
        yield self.y_damagePlayer(self.getEnemySideTuple(), 1000)
        return True
