# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Forged Orc Whelp
卡名:锤炼小兽人
效果:1A:把自己卡组顶端1张卡送入弃牌区;是怪兽的场合,自己抽1张卡。
"""

class OrcPBR(Card):
    CARD_KEY = 'OrcPBR'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(OrcPBR_e1)


class OrcPBR_e1(Effect):
    # 1A:把自己卡组顶端1张卡送入弃牌区;是怪兽的场合,自己抽1张卡。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.drawCard]
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
        topCard = deck[-1]
        isMon = topCard.isMonster()
        yield self.y_sendCardToGrave(topCard)
        if isMon and len(self.game.decks[self.getSide()]) > 0:
            yield self.y_drawCard(self.getSide(), 1)
        return True

