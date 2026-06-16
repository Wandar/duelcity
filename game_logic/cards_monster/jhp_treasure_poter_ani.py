# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Treasure Seeker Squirrel
卡名:宝藏搜寻者
效果:1T:<召唤时>:查看卡组顶3张,把1张加入手牌,其余放回原位。
"""

class jhp_treasure_poter_ani(Card):
    CARD_KEY = 'jhp_treasure_poter_ani'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(jhp_treasure_poter_ani_e1)


class jhp_treasure_poter_ani_e1(Effect):
    # 1T:<召唤时>:查看卡组顶3张,把1张加入手牌,其余放回原位。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.earn]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        if len(self.game.decks[self.getSide()]) < 1:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        deck = self.game.decks[self.getSide()]
        top = list(reversed(deck[-3:]))
        if not top:
            return False
        chosen = yield self.y_select1Card(top, TITLE.addToHand, self.getSide(), canCancel=True)
        if chosen:
            yield self.y_returnCardToHand(chosen)
        return True

