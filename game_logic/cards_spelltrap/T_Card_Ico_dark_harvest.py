# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_dark_harvest  【陷阱】
卡图:蓝色背景,蓝色机械小人横躺黄色火焰上方,漂浮绿色音符能量,黑暗收割。
效果(AOTIP):
1OT:<对方怪兽被破坏后>:黑暗收割——自己回复300基本分,并对对方造成200伤害。
"""

class tT_Card_Ico_dark_harvest(Card):
    CARD_KEY = "T_Card_Ico_dark_harvest"
    AUTHOR = "Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_dark_harvest_eff)

class tT_Card_Ico_dark_harvest_eff(Effect):
    effType = EFF_TYPE.optionalTrigger
    observeSignals = (LOCATION.spellTrapZone, [Signal.Destroyed])
    AI_HINT = [AI_HINT.recoverLP, AI_HINT.damager]
    EFF_POWER = 2

    def y_cost(self, justCheck: bool, signal):
        if not isSignal(signal, Signal.Destroyed): return False
        dead = signal.card
        if dead is None or not dead.isMonster(): return False
        if dead.side not in self.getEnemySideTuple(): return False
        if not self.owner.isInSpellZone(): return False
        if justCheck: return True
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck: return True
        yield self.y_healPlayer(self.getSide(), 300)
        yield self.y_damagePlayer(self.getEnemySideTuple(), 200)
        return True
