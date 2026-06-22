# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Emerald Crystal Lizard
卡名:碧空晶蜥
效果:1P:此卡攻击守备表示怪兽时给予贯通伤害。2T:<召唤·特殊召唤时>:破坏对方场上1张魔法·陷阱卡。
"""

class Wyrm1_2(Card):
    CARD_KEY = 'Wyrm1_2'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Wyrm1_2_e1)
        self.initEffect(Wyrm1_2_e2)


class Wyrm1_2_e1(Effect):
    # 1P:此卡攻击守备表示怪兽时给予贯通伤害。
    # NOTE: "贯通" 暂无钩子,登记为常驻标记效果,待战斗结算查询。
    effType = EFF_TYPE.permanent
    observeSignals = (LOCATION.monsterZone, [Signal.AttachMonsterZone, Signal.DetachMonsterZone])
    AI_HINT = [AI_HINT.permanent, AI_HINT.battleBenefit]
    EFF_POWER = 3

    def y_signal(self, signal):
        return
        yield


class Wyrm1_2_e2(Effect):
    # 2T:<召唤·特殊召唤时>:破坏对方场上1张魔法·陷阱卡。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.spellDestroyer]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        enemyST = self.searchCards(LOCATION.spellTrapZone, self.getEnemySideTuple(), CARD_TYPE.all, self)
        if not enemyST:
            return False
        if justCheck:
            return True
        t = yield self.y_select1Card(enemyST, TITLE.destroy, canCancel=True)
        if not t:
            return False
        self.saveTarget1(t)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1()
        if not t:
            return False
        yield self.y_destroyCard(t)
        return True
