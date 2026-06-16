# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Kingspike Wasp
卡名:毒刺蜂王
效果:1A:[把自己场上1只其他昆虫族怪兽送入弃牌区]:对对手造成600点伤害。
"""

class Wasp_Blue(Card):
    CARD_KEY = 'Wasp_Blue'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Wasp_Blue_e1)


class Wasp_Blue_e1(Effect):
    # 1A:[把自己场上1只其他昆虫族怪兽送入弃牌区]:对对手造成600点伤害。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.damager, AI_HINT.costMonster]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        def isFodder(c):
            return c != self.owner and c.race == RACE.INSECT
        fodder = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self, isFodder)
        if not fodder:
            return False
        if justCheck:
            return True
        cost = yield self.y_select1Card(fodder, TITLE.sendToGrave, canCancel=True)
        if not cost:
            return False
        yield self.y_sendCardToGrave(cost)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        yield self.y_damagePlayer(self.getEnemySideTuple(), 600)
        return True

