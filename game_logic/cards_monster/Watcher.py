# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Watcher
卡名:观察者
效果:1T:<召唤后>:确认对方的手牌。2A:猜测对方卡组顶端的卡的种类,猜对的情况自己抽1张卡,猜错的情况把该卡送入对方手牌。
"""

class Watcher(Card):
    CARD_KEY = 'Watcher'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Watcher_e1)
        self.initEffect(Watcher_e2)


class Watcher_e1(Effect):
    # 1T:<召唤后>:确认对方的手牌。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.search]
    EFF_POWER = 1

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        oppHand = self.searchCards(LOCATION.hand, self.getEnemySideTuple(), CARD_TYPE.all, None)
        if oppHand:
            yield self.y_select1Card(oppHand, TITLE.target, self.getSide(), canCancel=True)
        return True


class Watcher_e2(Effect):
    # 2A:猜测对方卡组顶端的卡的种类,猜对自己抽1张卡,猜错把该卡送入对方手牌。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.drawCard]
    EFF_POWER = 2

    def y_cost(self, justCheck, signal):
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
            if len(self.game.decks[self.getSide()]) > 0:
                yield self.y_drawCard(self.getSide(), 1)
        else:
            yield self.y_returnCardToHand(topCard)
        return True

