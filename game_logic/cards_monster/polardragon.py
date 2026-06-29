# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Polar Ice Dragon
卡名:冰晶之龙
效果:1T:<召唤时>:对方场上1只怪兽沉默,且不能攻击。2P:此卡被攻击的伤害计算时,对攻击怪兽造成500点伤害。
"""

class polardragon(Card):
    CARD_KEY = 'polardragon'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(polardragon_e1)
        self.initEffect(polardragon_e2)


class polardragon_e1(Effect):
    # 1T:<召唤时>:对方场上1只怪兽沉默,且不能攻击。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.debuff]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        enemies = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self)
        if not enemies:
            return False
        if justCheck:
            return True
        chosen = yield self.y_select1Card(enemies, TITLE.target, canCancel=False)
        if not chosen:
            return False
        self.saveTarget1(chosen)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1()
        if not t:
            return False
        # 沉默(无效效果)且不能攻击
        yield self.y_silenceCard(t, effDuration=EFF_DURATION.onceForever)
        if t.isMonsterOnField():
            yield self.y_changeCardData(t, newAttackTimes=0, effDuration=EFF_DURATION.onceForever)
        return True


class polardragon_e2(Effect):
    # 2P:此卡被攻击的伤害计算时,对攻击怪兽造成500点伤害。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.InBattle])
    AI_HINT = [AI_HINT.damager]
    EFF_POWER = 3
    countLimit = COUNT_LIMIT.unlimited

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.InBattle):
            return False
        # 仅当此卡是被攻击的一方
        if signal.receiverCard != self.owner:
            return False
        attacker = signal.attackerCard
        if attacker is None or type(attacker) == int or not attacker.isMonsterOnField():
            return False
        if justCheck:
            return True
        self.saveTarget1(attacker)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        attacker = self.getLegalTarget1()
        if not attacker or not attacker.isMonsterOnField():
            return False
        yield self.y_damageCard(attacker, 500)
        return True
