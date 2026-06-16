# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Were Anglerfish
卡名:鱼人安康
效果:1A:宣言1个等级,翻开自己卡组顶端1张卡,是该等级的怪兽则将其特殊召唤,否则送入弃牌区。
"""

class weranglerfish(Card):
    CARD_KEY = 'weranglerfish'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(weranglerfish_e1)


class weranglerfish_e1(Effect):
    # 1A:宣言1个等级,翻开卡组顶端1张:是该等级的怪兽则特殊召唤,否则送墓。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 3

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
        levels = [str(i) for i in range(1, 13)]
        option = yield self.y_showOptionsPopUp("title_target", "title_target", self.getSide(), levels, 0)
        wantLevel = option + 1
        topCard = deck[-1]
        if topCard.isMonster() and topCard.level == wantLevel and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(topCard)
        else:
            yield self.y_sendCardToGrave(topCard)
        return True

