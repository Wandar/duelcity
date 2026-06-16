# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Ironwall Vanguard
卡名:铁壁推进者
效果:1A:[把此卡解放]:从卡组把1只机械族怪兽以守备表示特殊召唤。
"""

class Assault_Mech_Skin1(Card):
    CARD_KEY = 'Assault Mech_Skin1'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Assault_Mech_Skin1_e1)


class Assault_Mech_Skin1_e1(Effect):
    # 1A:[把此卡解放]:从卡组把1只机械族怪兽以守备表示特殊召唤。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        def isTarget(c):
            return c.race == RACE.MACHINE
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
        yield self.y_specialSummon(t, form=FORM.defence)
        return True

