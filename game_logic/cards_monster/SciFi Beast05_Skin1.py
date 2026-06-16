# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Mechabeast Rex
卡名:百兽机 暴龙
效果:1T:<召唤时>:破坏对方场上1只怪兽,此卡本回合不能攻击。
"""

class SciFi_Beast05_Skin1(Card):
    CARD_KEY = 'SciFi Beast05_Skin1'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(SciFi_Beast05_Skin1_e1)


class SciFi_Beast05_Skin1_e1(Effect):
    # 1T:<召唤时>:破坏对方场上1只怪兽,此卡本回合不能攻击。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 4

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        enemies = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self)
        if not enemies:
            return False
        if justCheck:
            return True
        t = yield self.y_select1Card(enemies, TITLE.destroy, canCancel=True)
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
        # 本回合不能攻击(攻击次数置0近似)
        if self.owner.isMonsterOnField():
            yield self.y_changeCardData(self.owner, newAttackTimes=0, effDuration=EFF_DURATION.utilTurnEnds)
        return True

