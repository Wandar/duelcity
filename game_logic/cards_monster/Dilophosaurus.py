# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Dilophosaurus
卡名:双冠龙
效果:1T:<召唤时>:破坏对方场上1只怪兽,此卡本回合不能攻击。
"""

class Dilophosaurus(Card):
    CARD_KEY = "Dilophosaurus"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Dilophosaurus_e1)


class Dilophosaurus_e1(Effect):
    # 1T:<召唤时>:破坏对方场上1只怪兽,此卡本回合不能攻击。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        enemies = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(),
                                   CARD_TYPE.monster, self)
        if not enemies:
            return False
        if justCheck:
            return True
        chosen = yield self.y_select1Card(enemies, TITLE.destroy, canCancel=False)
        if not chosen:
            return False
        self.saveTarget1(chosen)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        target = self.getLegalTarget1()
        if not target:
            return False
        yield self.y_destroyCard(target)
        # 此卡本回合不能攻击
        if self.owner.isMonsterOnField():
            yield self.y_changeCardData(self.owner, newAttackTimes=0, effDuration=EFF_DURATION.utilTurnEnds)
        return True
