# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Fire Dragon
卡名:火龙
effect:
效果:1A:翻开自己卡组顶端5张卡,把最先找到的LV5以下的炎属性怪兽特殊召唤,其余的卡以原来的顺序放回原位.
"""

class FireDragonRed(Card):
    CARD_KEY = "FireDragonRed"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(FireDragonRed_e1)


class FireDragonRed_e1(Effect):
    # 1A:翻开自己卡组顶端5张卡,把最先找到的LV5以下的炎属性怪兽特殊召唤,其余的卡以原来的顺序放回原位.
    effType = EFF_TYPE.active
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if self.getDeckLeftNum() == 0:
            return False
        if self.freeMonsterSpace() == 0:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        deck = self.game.decks[self.getSide()]
        # the top of the deck is the last element; scan the top 5 from the very top downward
        top5 = list(reversed(deck[-5:]))
        target = None
        for c in top5:
            if (c.cardType & CARD_TYPE.monster) and c.attr == ATTR.FIRE and c.level <= 5:
                target = c
                break
        if target and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(target)
        return True
