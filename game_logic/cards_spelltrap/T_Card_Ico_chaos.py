# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
import random as _r
"""
CardName:T_Card_Ico_chaos  【魔法】
卡图:粉蓝鲜艳背景,两个小角色激烈对打,冰块与能量四散,场面混乱。
效果(AOTIP):
1A:混乱降临——双方场上各随机破坏1张卡,且双方各随机丢弃1张手卡。
"""

class tT_Card_Ico_chaos(Card):
    CARD_KEY = "T_Card_Ico_chaos"
    AUTHOR = "Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_chaos_eff)

class tT_Card_Ico_chaos_eff(Effect):
    effType = EFF_TYPE.active
    activateLocation = LOCATION.spellTrapZone
    AI_HINT = [AI_HINT.eraser, AI_HINT.targetAll]
    EFF_POWER = 3

    def y_cost(self, justCheck: bool, signal):
        if justCheck: return True
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck: return True
        for s in tuple(self.game.monsters.keys()):
            field = self.searchCards(LOCATION.monsterZone | LOCATION.spellTrapZone,
                                     (s,), CARD_TYPE.all, self)
            if field:
                yield self.y_destroyCard(_r.choice(field))
            hand = self.searchCards(LOCATION.hand, (s,), CARD_TYPE.all, self)
            if hand:
                yield self.y_sendCardToGrave(_r.choice(hand))
        return True
