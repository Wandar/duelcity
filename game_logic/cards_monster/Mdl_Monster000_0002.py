# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Rainbow Featherstorm Dragon
卡名:虹羽风暴龙
效果:1P:此卡1回合可对对方场上每只怪兽各攻击1次;被此卡战斗破坏的怪兽其效果在墓地也无效。
"""

class Mdl_Monster000_0002(Card):
    CARD_KEY = 'Mdl_Monster000_0002'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Mdl_Monster000_0002_e1)


class Mdl_Monster000_0002_e1(Effect):
    # 1P:此卡1回合可对对方场上每只怪兽各攻击1次;被此卡战斗破坏的怪兽其效果在墓地也无效。
    # NOTE: 多重攻击以提高攻击次数近似(上限5);"墓地效果无效"暂无钩子。
    effType = EFF_TYPE.permanent
    observeSignals = (LOCATION.monsterZone, [Signal.AttachMonsterZone, Signal.DetachMonsterZone])
    AI_HINT = [AI_HINT.permanent, AI_HINT.battleBenefit]
    EFF_POWER = 5

    def y_signal(self, signal):
        if isSignal(signal, Signal.DetachMonsterZone, self.owner):
            yield self.y_removeBuffEffectSource(self.owner, self.effUniID)
            return
        if not self.owner.isMonsterOnField():
            return
        yield self.y_changeCardData(self.owner, newAttackTimes=5,
                                    effDuration=EFF_DURATION.fromSource, uniqueSourceID=self.effUniID)

