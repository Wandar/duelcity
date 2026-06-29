# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Mechabeast Whale
卡名:百兽机 黑鲸
效果:1A:[把此卡解放]:发现一张等级3以下的机械族怪兽并守备召唤。
"""

class SciFi_Beast04_WhaleSnake_Skin1(Card):
    CARD_KEY = 'SciFi Beast04 WhaleSnake Skin1'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(SciFi_Beast04_WhaleSnake_Skin1_e1)


class SciFi_Beast04_WhaleSnake_Skin1_e1(Effect):
    # 1A:[把此卡解放]:发现一张等级3以下的机械族怪兽并守备召唤。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.summoner, AI_HINT.costMonster]
    EFF_POWER = 4

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
        picked = yield self.y_discoverCard(side=self.getSide(), race=RACE.MACHINE,
                                           cardType=CARD_TYPE.monster, maxLevel=3, count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked, form=FORM.defence)
        return True
