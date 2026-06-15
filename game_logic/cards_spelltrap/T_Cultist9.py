# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Cultist9  【魔法】
卡图:深紫背景,金黄三叉戟祭坛/圣杯矗立中央,飘出蓝色幽灵雾气,邪教仪式感。
效果(AOTIP):
1A:[解放自己场上1只怪兽]:献祭仪式——从自己卡组把1只7星以上怪兽加入手卡,并回复500基本分。
"""

class tT_Cultist9(Card):
    CARD_KEY = "T_Cultist9"
    AUTHOR = "Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Cultist9_eff)

class tT_Cultist9_eff(Effect):
    effType = EFF_TYPE.active
    activateLocation = LOCATION.spellTrapZone
    AI_HINT = [AI_HINT.searchMonster, AI_HINT.recoverLP]
    EFF_POWER = 3

    def _isHigh(self, c):
        return c.level >= 7

    def y_cost(self, justCheck: bool, signal):
        myMons = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self)
        cands = self.searchCards(LOCATION.deck, self.getSide(), CARD_TYPE.monster, self, self._isHigh)
        if not myMons or not cands: return False
        if justCheck: return True
        trib = yield self.y_select1Card(myMons, TITLE.tribute, self.getSide(), canCancel=True)
        if not trib: return False
        successNum = yield self.y_tributeCard(trib)
        if not successNum: return False
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck: return True
        cands = self.searchCards(LOCATION.deck, self.getSide(), CARD_TYPE.monster, self, self._isHigh)
        if cands:
            t = yield self.y_select1Card(cands, TITLE.addToHand, self.getSide(), canCancel=True)
            if t:
                yield self.y_returnCardToHand(t, self.getSide())
        yield self.y_healPlayer(self.getSide(), 500)
        return True
