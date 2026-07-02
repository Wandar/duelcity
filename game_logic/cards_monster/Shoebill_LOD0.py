# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Shoebill
卡名:鲸头鹳
效果:1A:[把此卡解放]:发现一张等级2以下的鸟兽族怪兽并守备召唤。
"""

class Shoebill_LOD0(Card):
    CARD_KEY = "Shoebill_LOD0"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Shoebill_LOD0_e1)


class Shoebill_LOD0_e1(Effect):
    # 1A:[把此卡解放]:发现一张等级2以下的鸟兽族怪兽并守备召唤。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.summoner, AI_HINT.costMonster]
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
        if self.freeMonsterSpace() == 0:
            return False
        picked = yield self.y_discoverCard(title=TITLE.specialSummon, side=self.getSide(), race=RACE.WINDBEAST,
                                           cardType=CARD_TYPE.monster, maxLevel=2, count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked, form=FORM.defence)
        return True
