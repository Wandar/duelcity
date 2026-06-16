# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Ladybug
卡名:瓢虫
效果:1T:<召唤时>:确认自己卡组顶端7张卡,把其中1只昆虫族怪兽加入手牌,其余的卡以任意顺序放回卡组顶端。
"""

class Ladybug(Card):
    CARD_KEY = 'Ladybug'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Ladybug_e1)


class Ladybug_e1(Effect):
    # 1T:<召唤时>:确认卡组顶7张,把其中1只昆虫族加入手牌,其余以任意顺序放回顶端。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.searchMonster]
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
        side = self.getSide()
        deck = self.game.decks[side]
        n = min(7, len(deck))
        top = list(reversed(deck[-n:]))  # top-first
        insects = [c for c in top if c.isMonster() and c.race == RACE.INSECT]
        chosen = None
        if insects:
            chosen = yield self.y_select1Card(insects, TITLE.addToHand, side, canCancel=True)
        if chosen:
            yield self.y_returnCardToHand(chosen)
        # 其余放回顶端(可重排)
        remain = [c for c in top if c is not chosen and c.location == LOCATION.deck]
        if len(remain) >= 2:
            ordered = yield self.y_selectCards(remain, TITLE.returnToDeck, side, len(remain), len(remain), None, False, hasOrder=True)
            if ordered:
                deck = self.game.decks[side]
                base = [c for c in deck if c not in ordered]
                self.game.decks[side] = base + list(reversed(ordered))
        return True

