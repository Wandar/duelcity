# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:hypnosis
卡名:hypnosis
"""
"""
1A:控制一只对方怪兽,直到回合结束,此回合自己无法额外召唤
"""
class thypnosis(Card):
    CARD_KEY="hypnosis"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(thypnosis_effect1)

class thypnosis_effect1(Effect):
    effType = EFF_TYPE.active

    AI_HINT = [AI_HINT.eraser]
    AI_POWER = 3

    def y_cost(self, justCheck:bool, signal):
        enemyMonsters = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(),
                                          CARD_TYPE.monster, self)
        if not enemyMonsters:
            return False
        if justCheck:
            return True
        target = yield self.y_select1Card(enemyMonsters, TITLE.target, canCancel=True)
        if target:
            self.saveTarget1(target)
            return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        target = self.getLegalTarget1()
        if target:
            yield self.y_controlCard(target, self.getSide(), EFF_DURATION.utilTurnEnds)
            self.owner.setData("hypnosisTurn", str(self.game.curTurn))
        return True
