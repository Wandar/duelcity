# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Lizard Warrior
卡名:蜥蜴战士
效果:1T:<战斗破坏对方怪兽时>:此卡攻击力+300直到回合结束。
"""

class LizardWarriorDefault(Card):
    CARD_KEY = 'LizardWarriorDefault'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(LizardWarriorDefault_e1)


class LizardWarriorDefault_e1(Effect):
    # 1T:<战斗破坏对方怪兽时>:此卡攻击力+300直到回合结束。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.BattleFinish])
    AI_HINT = [AI_HINT.addAtk]
    EFF_POWER = 2

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.BattleFinish):
            return False
        if signal.attackerCard != self.owner:
            return False
        rc = signal.receiverCard
        if rc is None or rc.isMonsterOnField():
            return False
        if not self.owner.isMonsterOnField():
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        yield self.y_addCardData(self.owner, attackAdd=300, effDuration=EFF_DURATION.utilTurnEnds)
        return True

