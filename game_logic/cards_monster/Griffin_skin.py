# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Gloomywood Guardian, Griffin of the Thicket
卡名:幽暗森林 守林狮鹫
效果:1T:<召唤时>:可破坏对方场上1张盖卡。
"""

class Griffin_skin(Card):
    CARD_KEY = 'Griffin_skin'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Griffin_skin_e1)


class Griffin_skin_e1(Effect):
    # 1T:<召唤时>:可破坏对方场上1张盖卡。
    effType = EFF_TYPE.optionalTrigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.spellDestroyer]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        def isSet(c):
            return c.form & FORM.set != 0
        sets = self.searchCards(LOCATION.spellTrapZone, self.getEnemySideTuple(), CARD_TYPE.all, self, isSet)
        if not sets:
            return False
        if justCheck:
            return True
        t = yield self.y_select1Card(sets, TITLE.destroy, canCancel=True)
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

