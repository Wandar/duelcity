# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Flower-Crowned Piglet
卡名:花冠小猪
效果:1T:<召唤时>:把自己卡组顶端1张卡送入弃牌区;是植物族怪兽的场合,将其特殊召唤。
"""

class ms07_Wildboar_1(Card):
    CARD_KEY = 'ms07_Wildboar_1'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(ms07_Wildboar_1_e1)


class ms07_Wildboar_1_e1(Effect):
    # 1T:<召唤时>:把自己卡组顶端1张卡送入弃牌区;是植物族怪兽的场合,将其特殊召唤。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 2

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
        if not deck:
            return False
        topCard = deck[-1]
        isPlant = topCard.isMonster() and topCard.race == RACE.PLANT
        if isPlant and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(topCard)
        else:
            yield self.y_sendCardToGrave(topCard)
        return True

