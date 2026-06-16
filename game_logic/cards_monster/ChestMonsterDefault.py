# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Chest Monster
卡名:宝箱怪
效果:1T:<被战斗破坏后>:翻开自己卡组顶端的卡:魔法卡则加入手牌;怪兽则将其临时召唤;陷阱卡则对破坏此卡的玩家造成800点伤害。
"""

class ChestMonsterDefault(Card):
    CARD_KEY = 'ChestMonsterDefault'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(ChestMonsterDefault_e1)


class ChestMonsterDefault_e1(Effect):
    # 1T:<被战斗破坏后>:翻开卡组顶:魔法→手牌;怪兽→临时召唤;陷阱→对凶手造成800伤害。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.grave, [Signal.DestroyedByBattle])
    AI_HINT = [AI_HINT.earn]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.DestroyedByBattle, self.owner):
            return False
        if len(self.game.decks[self.getSide()]) < 1:
            return False
        if justCheck:
            return True
        self._killer = getattr(signal, "reasonCard", None)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        deck = self.game.decks[self.getSide()]
        if not deck:
            return False
        topCard = deck[-1]
        if topCard.isSpell():
            yield self.y_returnCardToHand(topCard)
        elif topCard.isMonster():
            if self.freeMonsterSpace() > 0:
                yield self.y_specialSummon(topCard, buffIDOrList=CARD_BUFF.temporary)
        elif topCard.isTrap():
            killer = getattr(self, "_killer", None)
            side = killer.side if killer else self.getEnemySideTuple()[0]
            yield self.y_damagePlayer(side, 800)
        return True

