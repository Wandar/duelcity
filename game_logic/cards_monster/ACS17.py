# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:ACS17
卡名:机甲17
效果:1A:[把1张手牌送入弃牌区]:从卡组检索1只等级4以下的机械族怪兽并覆盖。
"""

class ACS17(Card):
    CARD_KEY = 'ACS17'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(ACS17_e1)


class ACS17_e1(Effect):
    # 1A:[把1张手牌送入弃牌区]:从卡组检索1只等级4以下的机械族怪兽并覆盖(面朝下守备召唤)。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.summoner, AI_HINT.costHand]
    EFF_POWER = 2

    def y_cost(self, justCheck, signal):
        hand = self.searchCards(LOCATION.hand, self.getSide(), CARD_TYPE.all, self)
        if not hand:
            return False
        def isT(c):
            return c.race == RACE.MACHINE and c.level <= 4
        targets = self.searchCards(LOCATION.deck, self.getSide(), CARD_TYPE.monster, self, isT)
        if not targets:
            return False
        if self.freeMonsterSpace() == 0:
            return False
        if justCheck:
            return True
        cost = yield self.y_select1Card(hand, TITLE.sendToGrave, canCancel=True)
        if not cost:
            return False
        chosen = yield self.y_select1Card(targets, TITLE.specialSummon, canCancel=True)
        if not chosen:
            return False
        yield self.y_sendCardToGrave(cost)
        self.saveTarget1(chosen)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1(checkLocationChange=False)
        if not t or self.freeMonsterSpace() == 0:
            return False
        # 覆盖:面朝下以守备表示放置
        yield self.y_specialSummon(t, form=FORM.defenceSet)
        return True
