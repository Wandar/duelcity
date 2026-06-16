# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Lizard Merchant
卡名:蜥蜴商人
效果:1A:[宣言1种卡的种类]:翻开自己卡组顶端的卡,一致则加入手牌;不一致则把该卡送入弃牌区,自己回复500基本分。
"""

class Lizard_Green(Card):
    CARD_KEY = 'Lizard_Green'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Lizard_Green_e1)


class Lizard_Green_e1(Effect):
    # 1A:[宣言1种卡的种类]:翻开自己卡组顶端的卡,一致则加入手牌;不一致则送墓并回复500。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.earn]
    EFF_POWER = 2

    def y_cost(self, justCheck, signal):
        if len(self.game.decks[self.getSide()]) < 1:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        deck = self.game.decks[self.getSide()]
        if not deck:
            return False
        option = yield self.y_showOptionsPopUp("title_target", "title_target", self.getSide(),
                                               ["MONSTER", "SPELL", "TRAP"], 0)
        wantType = (CARD_TYPE.monster, CARD_TYPE.spell, CARD_TYPE.trap)[option]
        topCard = deck[-1]
        if topCard.type == wantType:
            yield self.y_returnCardToHand(topCard)
        else:
            yield self.y_sendCardToGrave(topCard)
            yield self.y_healPlayer(self.getSide(), 500)
        return True

