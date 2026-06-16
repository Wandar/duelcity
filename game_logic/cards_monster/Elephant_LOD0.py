# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Spirit Trunk Elephant
卡名:灵鼻象
效果:1T:<召唤时>:宣言1种卡的种类,确认对方卡组顶端1张卡:种类一致的场合将其送入弃牌区。
"""

class Elephant_LOD0(Card):
    CARD_KEY = 'Elephant_LOD0'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Elephant_LOD0_e1)


class Elephant_LOD0_e1(Effect):
    # 1T:<召唤时>:宣言1种卡的种类,确认对方卡组顶端1张卡:种类一致的场合将其送入弃牌区。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 2

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        enemy = self.getEnemySideTuple()[0]
        if len(self.game.decks[enemy]) < 1:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        enemy = self.getEnemySideTuple()[0]
        deck = self.game.decks[enemy]
        if not deck:
            return False
        option = yield self.y_showOptionsPopUp("title_target", "title_target", self.getSide(),
                                               ["MONSTER", "SPELL", "TRAP"], 0)
        wantType = (CARD_TYPE.monster, CARD_TYPE.spell, CARD_TYPE.trap)[option]
        topCard = deck[-1]
        if topCard.type == wantType:
            yield self.y_sendCardToGrave(topCard)
        return True

