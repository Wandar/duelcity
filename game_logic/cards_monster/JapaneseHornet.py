# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Japanese Hornet
卡名:日本大黄蜂
效果:1A:[把自己场上的此卡返回手牌]:对对方场上1只怪兽造成600点伤害。
"""

class JapaneseHornet(Card):
    CARD_KEY = 'JapaneseHornet'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(JapaneseHornet_e1)


class JapaneseHornet_e1(Effect):
    # 1A:[把自己场上的此卡返回手牌]:对对方场上1只怪兽造成600点伤害。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.damager]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        enemies = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self)
        if not enemies:
            return False
        if justCheck:
            return True
        t = yield self.y_select1Card(enemies, TITLE.damage, canCancel=True)
        if not t:
            return False
        self.saveTarget1(t)
        yield self.y_returnCardToHand(self.owner)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1(checkLocationChange=False)
        if not t or not t.isMonsterOnField():
            return False
        yield self.y_damageCard(t, 600)
        return True

