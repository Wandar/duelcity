# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Gilded Mechbone Dragon
卡名:黄金机骸龙
效果:1T:<此卡被特殊召唤时>:从卡组发现一张卡并覆盖。2T:<我方准备阶段>:此卡攻击力·守备力上升400。
"""

class Dragon7_basemesh1(Card):
    CARD_KEY = 'Dragon7_basemesh1'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Dragon7_basemesh1_e1)
        self.initEffect(Dragon7_basemesh1_e2)


class Dragon7_basemesh1_e1(Effect):
    # 1T:<此卡被特殊召唤时>:从卡组发现一张卡并覆盖。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.SpecialSummon])
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.SpecialSummon, self.owner):
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        picked = yield self.y_discoverCard(side=self.getSide(), cardType=CARD_TYPE.all, count=3, canCancel=True)
        if not picked:
            return True
        if picked.isMonster():
            if self.freeMonsterSpace() > 0:
                yield self.y_specialSummon(picked, form=FORM.defenceSet)
        else:
            yield self.y_setCardToSpellZone(picked, self.getSide())
        return True


class Dragon7_basemesh1_e2(Effect):
    # 2T:<我方准备阶段>:此卡攻击力·守备力上升400。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.StandbyPhase])
    AI_HINT = [AI_HINT.enhance]
    EFF_POWER = 2
    countLimit = COUNT_LIMIT.unlimited

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.StandbyPhase):
            return False
        if self.game.whoseTurn != self.getSide():
            return False
        if not self.owner.isMonsterOnField():
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        yield self.y_addCardData(self.owner, attackAdd=400, defenceAdd=400, effDuration=EFF_DURATION.onceForever)
        return True
