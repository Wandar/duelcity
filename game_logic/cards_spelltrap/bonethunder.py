# -*- coding: utf-8 -*-
from __future__ import annotations
import random
from dutil import *
from annos import *
"""
CardName:Undying Thunder
卡名:亡骸雷击
effect:
效果:1A:选择自己场上一只等级4以下的怪兽,从卡组·弃牌区特殊召唤最多两张同名卡,然后对自己场上所有怪兽造成500点伤害
"""

class tbonethunder(Card):
    CARD_KEY = "bonethunder"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(tbonethunder_effect1)


class tbonethunder_effect1(Effect):
    # 1A:选择自己场上一只等级4以下的怪兽,从卡组·弃牌区特殊召唤最多两张同名卡,然后对自己场上所有怪兽造成500点伤害
    effType = EFF_TYPE.active
    AI_HINT = [AI_HINT.summoner]
    AI_POWER = 3

    def y_cost(self, justCheck, signal):
        myLV4 = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self,
                                 lambda c: c.level <= 4)
        if not myLV4:
            return False
        if justCheck:
            return True
        target = yield self.y_select1Card(myLV4, TITLE.target, canCancel=True)
        if not target:
            return False
        self.saveTarget1(target)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        base = self.getLegalTarget1()
        if not base:
            return False
        sameNameCards = self.searchCards(LOCATION.deck, self.getSide(), CARD_TYPE.monster, self,
                                         lambda c: c.cardKey == base.cardKey)
        sameNameCards += self.searchCards(LOCATION.grave, self.getSide(), CARD_TYPE.monster, self,
                                          lambda c: c.cardKey == base.cardKey and c.canSpecialSummon())
        random.shuffle(sameNameCards)
        for card in sameNameCards[:2]:
            if self.freeMonsterSpace() == 0:
                break
            yield self.y_specialSummon(card)
        myMonsters = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self)
        if myMonsters:
            yield self.y_damageCard(myMonsters, 500)
        return True
