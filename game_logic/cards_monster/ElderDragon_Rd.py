# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Lava Dragon King
卡名:熔岩圣龙
效果:1A:[把自己场上1只"熔岩"怪兽解放]:从手牌·卡组把1只"金焰熔岩龙"特殊召唤。
"""

class ElderDragon_Rd(Card):
    CARD_KEY = 'ElderDragon_Rd'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(ElderDragon_Rd_e1)


class ElderDragon_Rd_e1(Effect):
    # 1A:[把自己场上1只"熔岩"怪兽解放]:从手牌·卡组把1只"金焰熔岩龙"特殊召唤。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.summoner, AI_HINT.costMonster]
    EFF_POWER = 4

    def y_cost(self, justCheck, signal):
        lava = ("smallDragonWhelp_Rd", "Dragon_Rd", "ElderDragon_Rd", "Mdl_Monster000_0000")
        def isLava(c):
            return c.cardKey in lava
        fodder = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self, isLava)
        if not fodder:
            return False
        def isTarget(c):
            return c.cardKey == "Mdl_Monster000_0000"
        targets = self.searchCards(LOCATION.hand | LOCATION.deck, self.getSide(), CARD_TYPE.monster, self, isTarget)
        if not targets:
            return False
        if justCheck:
            return True
        cost = yield self.y_select1Card(fodder, TITLE.tribute, canCancel=True)
        if not cost:
            return False
        chosen = yield self.y_select1Card(targets, TITLE.specialSummon, canCancel=True)
        if not chosen:
            return False
        successNum = yield self.y_tributeCard(cost)
        if not successNum:
            return False
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

