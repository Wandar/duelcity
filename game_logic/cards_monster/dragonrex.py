# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Dragonrex
卡名:恐暴龙
效果:1T:<召唤时>:破坏自己场上此卡以外所有怪兽。2P:此卡每回合必须攻击。
注:2P「每回合必须攻击」由战斗系统读取怪兽的 mustAttack 标记执行;此处负责设置该标记。
"""

class dragonrex(Card):
    CARD_KEY = 'dragonrex'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(dragonrex_e1)
        self.initEffect(dragonrex_e2)


class dragonrex_e1(Effect):
    # 1T:<召唤时>:破坏自己场上此卡以外所有怪兽。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.eraser, AI_HINT.costMonster]
    EFF_POWER = 2

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        def isOther(c):
            return c != self.owner
        targets = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self, isOther)
        if not targets:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        def isOther(c):
            return c != self.owner
        targets = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self, isOther)
        if targets:
            yield self.y_destroyCard(list(targets))
        return True


class dragonrex_e2(Effect):
    # 2P:此卡每回合必须攻击。在此卡上设置 mustAttack 标记,供战斗系统判定。
    effType = EFF_TYPE.permanent
    observeSignals = (LOCATION.monsterZone, [Signal.AttachMonsterZone, Signal.DetachMonsterZone])
    AI_HINT = [AI_HINT.permanent]
    EFF_POWER = 1

    def y_signal(self, signal):
        if isSignal(signal, Signal.DetachMonsterZone, self.owner):
            self.owner.delData("mustAttack")
            return
        if self.owner.isMonsterOnField():
            self.owner.setData("mustAttack", "1")
        return
        yield
