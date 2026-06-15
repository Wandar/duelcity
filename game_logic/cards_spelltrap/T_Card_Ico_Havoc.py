# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
import random as _r
"""
CardName:T_Card_Ico_Havoc  【魔法】
卡图:紫底中央漆黑旋涡空洞,环绕亮粉/玫红弧形能量环,碎片飞散,破坏力十足。
效果(AOTIP):
1A:[支付1000]:浩劫旋涡——随机破坏对方场上最多2张卡,每破坏1张对对方造成300伤害。
"""

class tT_Card_Ico_Havoc(Card):
    CARD_KEY = "T_Card_Ico_Havoc"
    AUTHOR = "Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_Havoc_eff)

class tT_Card_Ico_Havoc_eff(Effect):
    effType = EFF_TYPE.active
    activateLocation = LOCATION.spellTrapZone
    AI_HINT = [AI_HINT.eraser, AI_HINT.damager]
    EFF_POWER = 3

    def y_cost(self, justCheck: bool, signal):
        if self.game.LPs[self.getSide()] <= 1000: return False
        cards = self.searchCards(LOCATION.monsterZone | LOCATION.spellTrapZone,
                                 self.getEnemySideTuple(), CARD_TYPE.all, self)
        if not cards: return False
        if justCheck: return True
        yield self.y_damagePlayer(self.getSide(), 1000)
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck: return True
        cards = self.searchCards(LOCATION.monsterZone | LOCATION.spellTrapZone,
                                 self.getEnemySideTuple(), CARD_TYPE.all, self)
        if not cards: return False
        chosen = _r.sample(cards, min(2, len(cards)))
        yield self.y_destroyCard(chosen)
        destroyed = sum(1 for c in chosen if not c.isOnField())
        if destroyed > 0:
            yield self.y_damagePlayer(self.getEnemySideTuple(), destroyed*300)
        return True
