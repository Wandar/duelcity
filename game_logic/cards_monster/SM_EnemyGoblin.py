# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Green Shade Murmurer
卡名:绿影咕哝者
效果:1A:[把此卡解放]:让对方随机丢弃1张手牌。
"""

class SM_EnemyGoblin(Card):
    CARD_KEY = 'SM_EnemyGoblin'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(SM_EnemyGoblin_e1)


class SM_EnemyGoblin_e1(Effect):
    # 1A:[把此卡解放]:让对方随机丢弃1张手牌。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.botDontUse]
    EFF_POWER = 2

    def y_cost(self, justCheck, signal):
        enemy = self.getEnemySideTuple()[0]
        oppHand = self.searchCards(LOCATION.hand, (enemy,), CARD_TYPE.all, None)
        if not oppHand:
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
        import random
        enemy = self.getEnemySideTuple()[0]
        oppHand = self.searchCards(LOCATION.hand, (enemy,), CARD_TYPE.all, None)
        if not oppHand:
            return False
        card = random.choice(oppHand)
        yield self.y_sendCardToGrave(card)
        return True

