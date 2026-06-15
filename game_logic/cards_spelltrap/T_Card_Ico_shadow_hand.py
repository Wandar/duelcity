# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
import random as _r
"""
CardName:T_Card_Ico_shadow_hand  【魔法】
卡图:深蓝夜空,蓝绿色发光龙爪从下方伸出,黑色树枝与新月,神秘。
效果(AOTIP):
1A:暗影之手——令对方随机1张手卡送入墓地(只破坏,不据为己有)。
"""

class tT_Card_Ico_shadow_hand(Card):
    CARD_KEY = "T_Card_Ico_shadow_hand"
    AUTHOR = "Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_shadow_hand_eff)

class tT_Card_Ico_shadow_hand_eff(Effect):
    effType = EFF_TYPE.active
    activateLocation = LOCATION.spellTrapZone
    AI_HINT = [AI_HINT.debuff]
    EFF_POWER = 2

    def y_cost(self, justCheck: bool, signal):
        enHand = self.searchCards(LOCATION.hand, self.getEnemySideTuple(), CARD_TYPE.all, self)
        if not enHand: return False
        if justCheck: return True
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck: return True
        enHand = self.searchCards(LOCATION.hand, self.getEnemySideTuple(), CARD_TYPE.all, self)
        if enHand:
            yield self.y_sendCardToGrave(_r.choice(enHand))
        return True
