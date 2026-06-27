# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Hunchbacked Ghoul
卡名:驼背食尸鬼
effect:
效果:1A:[丢弃1只不死族怪兽]:从自己手牌把1只等级3以下的不死族怪兽特殊召唤。
"""

class ghoul_grotesque(Card):
    CARD_KEY = "ghoul_grotesque"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(ghoul_grotesque_e1)


class ghoul_grotesque_e1(Effect):
    # 1A:[丢弃1只不死族怪兽]:从自己手牌把1只等级3以下的不死族怪兽特殊召唤。
    effType = EFF_TYPE.active
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if self.freeMonsterSpace() == 0:
            return False
        myHands = self.game.hands[self.getSide()]
        undeadHand = [c for c in myHands if (c.cardType & CARD_TYPE.monster) and c.race == RACE.UNDEAD]
        summonable = [c for c in undeadHand if c.level <= 3 and c.canSpecialSummon()]
        if not undeadHand or not summonable:
            return False
        if len(undeadHand) < 2 and undeadHand == summonable:
            return False
        if justCheck:
            return True

        discard = yield self.y_select1Card(undeadHand, TITLE.sendToGrave, canCancel=True)
        if not discard:
            return False
        summonChoices = [c for c in summonable if c is not discard]
        if not summonChoices:
            return False
        summonTarget = yield self.y_select1Card(summonChoices, TITLE.specialSummon, canCancel=True)
        if not summonTarget:
            return False
        yield self.y_sendCardToGrave(discard)
        self.saveTarget1(summonTarget)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        target = self.getLegalTarget1()
        if not target:
            return False
        yield self.y_specialSummon(target)
        return True
