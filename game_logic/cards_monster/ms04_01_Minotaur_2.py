# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Little Minotaur Warrior
卡名:牛头小战士
效果:1A:[把1张手牌送入弃牌区]:发现一张等级2以下的兽战士族怪兽并沉默召唤。
"""

class ms04_01_Minotaur_2(Card):
    CARD_KEY = 'ms04_01_Minotaur_2'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(ms04_01_Minotaur_2_e1)


class ms04_01_Minotaur_2_e1(Effect):
    # 1A:[把1张手牌送入弃牌区]:发现一张等级2以下的兽战士族怪兽并沉默召唤。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.summoner, AI_HINT.costHand]
    EFF_POWER = 4

    def y_cost(self, justCheck, signal):
        hand = self.searchCards(LOCATION.hand, self.getSide(), CARD_TYPE.all, self)
        if not hand:
            return False
        if self.freeMonsterSpace() == 0:
            return False
        if justCheck:
            return True
        cost = yield self.y_select1Card(hand, TITLE.discard, canCancel=True)
        if not cost:
            return False
        yield self.y_sendCardToGrave(cost)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        if self.freeMonsterSpace() == 0:
            return False
        picked = yield self.y_discoverCard(title=TITLE.specialSummon, side=self.getSide(), race=RACE.BEASTWARRIOR,
                                           cardType=CARD_TYPE.monster, maxLevel=2, count=3, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked)
            if picked.isMonsterOnField():
                yield self.y_silenceCard(picked, effDuration=EFF_DURATION.onceForever)
        return True
