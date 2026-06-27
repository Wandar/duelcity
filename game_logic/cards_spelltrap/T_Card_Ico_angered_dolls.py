# -*- coding: utf-8 -*-
from __future__ import annotations
import random
from dutil import *
from annos import *
"""
CardName:Angered Dolls
卡名:愤怒玩偶
effect:
效果:1A:选择场上一只等级4以下的恶魔族怪兽,从卡组·手牌额外召唤最多两张同名卡
"""

class tT_Card_Ico_angered_dolls(Card):
    CARD_KEY = "T_Card_Ico_angered_dolls"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(tT_Card_Ico_angered_dolls_effect1)


class tT_Card_Ico_angered_dolls_effect1(Effect):
    # 1A:选择场上一只等级4以下的恶魔族怪兽,从卡组·手牌额外召唤最多两张同名卡
    effType = EFF_TYPE.active
    AI_HINT = [AI_HINT.summoner]
    AI_POWER = 2

    def y_cost(self, justCheck, signal):
        targets = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self,
                                   lambda c: c.race == RACE.FIEND and c.level <= 4)
        if not targets:
            return False
        if justCheck:
            return True
        chosen = yield self.y_select1Card(targets, TITLE.target, canCancel=True)
        if not chosen:
            return False
        self.saveTarget1(chosen)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        base = self.getLegalTarget1()
        if not base:
            return False
        sameNameCards = self.searchCards(LOCATION.deck, self.getSide(), CARD_TYPE.monster, self,
                                         lambda c: c.cardKey == base.cardKey)
        sameNameCards += self.searchCards(LOCATION.hand, self.getSide(), CARD_TYPE.monster, self,
                                          lambda c: c.cardKey == base.cardKey and c.canSpecialSummon())
        random.shuffle(sameNameCards)
        for card in sameNameCards[:2]:
            if self.freeMonsterSpace() == 0:
                break
            yield self.y_specialSummon(card)
        return True
