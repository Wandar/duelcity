# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Pastureland Dragon
卡名:牧野之龙
效果:1T:<召唤时>:对对方场上所有怪兽各造成400点伤害。2T:<此卡战斗破坏对方怪兽时>:从手牌把1只等级4以下的怪兽特殊召唤。
"""

class plainsdragon(Card):
    CARD_KEY = 'plainsdragon'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(plainsdragon_e1)
        self.initEffect(plainsdragon_e2)


class plainsdragon_e1(Effect):
    # 1T:<召唤时>:对对方场上所有怪兽各造成400点伤害。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.damager]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        enemies = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self)
        if not enemies:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        enemies = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self)
        if enemies:
            yield self.y_damageCard(list(enemies), 400)
        return True


class plainsdragon_e2(Effect):
    # 2T:<此卡战斗破坏对方怪兽时>:从手牌把1只等级4以下的怪兽特殊召唤。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.BattleFinish])
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.BattleFinish):
            return False
        if signal.attackerCard != self.owner:
            return False
        rc = signal.receiverCard
        if rc is None or rc.isMonsterOnField():
            return False
        def isTarget(c):
            return c.level <= 4
        targets = self.searchCards(LOCATION.hand, self.getSide(), CARD_TYPE.monster, self, isTarget)
        if not targets:
            return False
        if self.freeMonsterSpace() == 0:
            return False
        if justCheck:
            return True
        chosen = yield self.y_select1Card(targets, TITLE.specialSummon, canCancel=True)
        if not chosen:
            return False
        self.saveTarget1(chosen)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1()
        if not t or self.freeMonsterSpace() == 0:
            return False
        yield self.y_specialSummon(t)
        return True
