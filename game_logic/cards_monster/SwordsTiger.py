# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Swords Tiger
卡名:剑虎
"""

class SwordsTiger(Card):
    CARD_KEY = "SwordsTiger"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(SwordsTiger_LightHunter)



"""
1I:与光属性怪兽战斗的场合，在伤害步骤内{ATK}+1000。
1I:<Battle effect>: When battling a LIGHT monster, gain 1000 ATK during the Damage Step.
"""
class SwordsTiger_LightHunter(Effect):
    effType = EFF_TYPE.instant

    observeSignals = (LOCATION.monsterZone, [Signal.InBattle])

    AI_HINT = [AI_HINT.addAtk]
    EFF_POWER = 3

    def y_activate(self, justCheck: bool, signal: Signal.InBattle):
        if not isSignal(signal, Signal.InBattle):
            return False
        myCard = None
        oppCard = None
        if signal.attackerCard == self.owner:
            myCard = signal.attackerCard
            oppCard = signal.receiverCard
        elif signal.receiverCard == self.owner:
            myCard = signal.receiverCard
            oppCard = signal.attackerCard
        else:
            return False
        if oppCard is None or oppCard.attr != ATTR.LIGHT:
            return False
        if not self.owner.isMonsterOnField():
            return False

        if justCheck:
            return True

        yield self.y_addCardData(
            self.owner, attackAdd=1000, effDuration=EFF_DURATION.utilBattleEnds,
        )
        return True
