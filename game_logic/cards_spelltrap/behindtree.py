# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:behindtree
卡名:behindtree
"""
"""
1I:当对方怪兽准备攻击时,从手牌·墓地特殊召唤一只LV4以下的怪兽
"""
class tbehindtree(Card):
    CARD_KEY="behindtree"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tbehindtree_effect1)

class tbehindtree_effect1(Effect):
    effType = EFF_TYPE.optionalInstant

    observeSignals = (LOCATION.spellTrapZone, [Signal.InBattle])

    AI_HINT = [AI_HINT.summoner]
    AI_POWER = 2

    def y_cost(self, justCheck:bool, signal:Signal.InBattle):
        if not (isSignal(signal, Signal.InBattle) and
                signal.attackerCard.side in self.getEnemySideTuple()):
            return False
        if not self.freeMonsterSpace():
            return False
        candidates = self.searchCards(LOCATION.hand, self.getSide(), CARD_TYPE.monster, self,
                                       lambda c: c.level <= 4)
        candidates += self.searchCards(LOCATION.grave, self.getSide(), CARD_TYPE.monster, self,
                                        lambda c: c.level <= 4 and c.canSpecialSummon())
        if not candidates:
            return False
        if justCheck:
            return True
        target = yield self.y_select1Card(candidates, TITLE.specialSummon, canCancel=True)
        if target:
            self.saveTarget1(target)
            return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        target = self.getLegalTarget1()
        if target:
            yield self.y_specialSummon(target)
        return True
