# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Unicorn Pegasus
卡名:独角兽珀加索斯
"""

class Unicorn_Pegasus(Card):
    CARD_KEY = "Unicorn_Pegasus"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Unicorn_Pegasus_LunarBind)


"""
1A:选择对手场上1只怪兽，使其攻击力变为0直到回合结束。
1A:<Field effect>:Target 1 monster your opponent controls; its ATK becomes 0 until the end of this turn.
"""
class Unicorn_Pegasus_LunarBind(Effect):
    effType = EFF_TYPE.active

    countLimit = COUNT_LIMIT.oncePerTurn
    activateLocation = LOCATION.monsterZone

    AI_HINT = [AI_HINT.debuff, AI_HINT.eraser]
    EFF_POWER = 3

    def y_cost(self, justCheck: bool, signal):
        enemies = self.searchCards(
            LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self
        )
        if not enemies:
            return False

        if justCheck:
            return True

        target = yield self.y_select1Card(enemies, TITLE.target, canCancel=True)
        if not target:
            return False

        self.saveTarget1(target)
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck:
            return True

        target = self.getLegalTarget1()
        if not target:
            return False

        yield self.y_changeCardData(
            target, newAtk=0, effDuration=EFF_DURATION.utilTurnEnds
        )
        return True
