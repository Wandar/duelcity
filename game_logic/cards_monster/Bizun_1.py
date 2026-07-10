# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Bramble Tusk Runt
卡名:棘丛小暴獠
效果:1A:[把1只我方怪兽返回手牌]:从手牌把1只等级2以下的兽族怪兽特殊召唤。
"""

class Bizun_1(Card):
    CARD_KEY = 'Bizun_1'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Bizun_1_e1)


class Bizun_1_e1(Effect):
    # 1A:[把1只我方怪兽返回手牌]:从手牌把1只等级2以下的兽族怪兽特殊召唤。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.summoner, AI_HINT.costMonster]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        def isT(c):
            return c.race == RACE.BEAST and c.level <= 2
        targets = self.searchCards(LOCATION.hand, self.getSide(), CARD_TYPE.monster, self, isT)
        if not targets:
            return False
        mine = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self)
        if not mine:
            return False
        if self.freeMonsterSpace() == 0:
            return False
        if justCheck:
            return True
        chosen = yield self.y_select1Card(targets, TITLE.specialSummon, canCancel=True)
        if not chosen:
            return False
        rc = yield self.y_select1Card(mine, TITLE.returnToHand, canCancel=True)
        if not rc:
            return False
        yield self.y_returnCardToHand(rc)
        self.saveTarget1(chosen)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1(checkLocationChange=False)
        if not t or self.freeMonsterSpace() == 0:
            return False
        yield self.y_specialSummon(t)
        return True
