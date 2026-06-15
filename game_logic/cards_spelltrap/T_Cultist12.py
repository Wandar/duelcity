# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Cultist12  【永续魔法】
卡图:深紫背景,黑袍人形俯身前倾,身体边缘蓝色电光,头顶紫色烟雾。
效果(AOTIP):
1T:<自己魔法效果发动时>:只要此卡在魔陷区,自己场上所有怪兽的{ATK}永久+200(诡术信徒的积累)。
"""

class tT_Cultist12(Card):
    CARD_KEY = "T_Cultist12"
    AUTHOR = "Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Cultist12_eff)

class tT_Cultist12_eff(Effect):
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.spellTrapZone, [Signal.BeforeActivateEffect])
    AI_HINT = [AI_HINT.addAtk]
    EFF_POWER = 2

    def y_cost(self, justCheck: bool, signal):
        if not isSignal(signal, Signal.BeforeActivateEffect): return False
        eff = signal.effect
        if not eff or eff is self: return False
        if not (eff.owner.cardType & CARD_TYPE.spell): return False
        if not self.checkAlly(eff.owner): return False
        if not self.owner.isInSpellZone(): return False
        myMons = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self)
        if not myMons: return False
        if justCheck: return True
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck: return True
        myMons = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self)
        if myMons:
            yield self.y_addCardData(myMons, attackAdd=200)
        return True
