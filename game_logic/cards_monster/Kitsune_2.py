# -*- coding: utf-8 -*-
from __future__ import annotations
import random
from dutil import *
from annos import *
"""
CardName:Raccoon Knight
卡名:浣熊骑士
效果:1A:[把此卡解放]:让对方随机丢弃1张手牌。
"""

class Kitsune_2(Card):
    CARD_KEY = 'Kitsune_2'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Kitsune_2_e1)


class Kitsune_2_e1(Effect):
    # 1A:[把此卡解放]:让对方随机丢弃1张手牌。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.costMonster]
    EFF_POWER = 2

    def y_cost(self, justCheck, signal):
        if not self.owner.isMonsterOnField():
            return False
        enemyHand = self.searchCards(LOCATION.hand, self.getEnemySideTuple(), CARD_TYPE.all, self)
        if not enemyHand:
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
        enemyHand = self.searchCards(LOCATION.hand, self.getEnemySideTuple(), CARD_TYPE.all, self)
        if not enemyHand:
            return False
        # 随机丢弃对方1张手牌
        chosen = random.choice(enemyHand)
        yield self.y_sendCardToGrave(chosen, chosen.side)
        return True
