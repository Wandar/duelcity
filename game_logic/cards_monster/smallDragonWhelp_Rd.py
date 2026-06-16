# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Lava Hatchling Dragon
卡名:熔岩雏龙
效果:1A:[把此卡解放]:从卡组把1只"熔岩绯龙"或"熔岩圣龙"特殊召唤,{ATK}+300。
"""

class smallDragonWhelp_Rd(Card):
    CARD_KEY = 'smallDragonWhelp_Rd'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(smallDragonWhelp_Rd_e1)


class smallDragonWhelp_Rd_e1(Effect):
    # 1A:[把此卡解放]:从卡组把1只"熔岩绯龙"或"熔岩圣龙"特殊召唤,该卡{ATK}+300。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 4

    def y_cost(self, justCheck, signal):
        def isTarget(c):
            return c.cardKey in ("Dragon_Rd", "ElderDragon_Rd")
        targets = self.searchCards(LOCATION.deck, self.getSide(), CARD_TYPE.monster, self, isTarget)
        if not targets:
            return False
        if justCheck:
            return True
        chosen = yield self.y_select1Card(targets, TITLE.specialSummon, canCancel=True)
        if not chosen:
            return False
        successNum = yield self.y_tributeCard(self.owner)
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
        if t.isMonsterOnField():
            yield self.y_addCardData(t, attackAdd=300, effDuration=EFF_DURATION.onceForever)
        return True

