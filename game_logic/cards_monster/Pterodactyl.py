# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Pterodactyl
卡名:翼手龙
效果:1T:<通常召唤时>:翻开自己卡组顶端3张卡,把其中的恐龙族怪兽全部覆盖到后场。
"""

class Pterodactyl(Card):
    CARD_KEY = 'Pterodactyl'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Pterodactyl_e1)


class Pterodactyl_e1(Effect):
    # 1T:<通常召唤时>:翻开自己卡组顶端3张卡,把其中的恐龙族怪兽全部覆盖到后场。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.NormalSummon])
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 4

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.NormalSummon, self.owner):
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
        top = list(reversed(deck[-3:]))
        dinos = [c for c in top if c.isMonster() and c.race == RACE.DINOSAUR]
        if dinos:
            # 把恐龙族怪兽作为面朝下的魔法·陷阱卡覆盖到后场
            yield self.y_setCardToSpellZone(dinos, side)
        return True

