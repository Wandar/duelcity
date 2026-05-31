# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Pterodactyl
卡名:翼手龙
"""

class Pterodactyl(Card):
    CARD_KEY = "Pterodactyl"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        # self.initEffect(Pterodactyl_SwiftNest)
        pass


"""
1P: <此卡在怪兽区时>: 我方每回合可以额外进行1次通常召唤。
    此卡离场时取消该额外召唤权利。
1P: <While this card is in the Monster Zone>:
    You may Normal Summon 1 additional time each turn.
    This bonus is lost when this card leaves the field.
"""
# class Pterodactyl_SwiftNest(Effect):
#     effType = EFF_TYPE.permanent
#
#     observeSignals = (LOCATION.monsterZone, [
#         Signal.AttachMonsterZone,
#         Signal.DetachMonsterZone,
#         Signal.StandbyPhase,
#     ])
#
#     AI_HINT = [AI_HINT.permanent, AI_HINT.summoner]
#     EFF_POWER = 3
#
#     def y_signal(self, signal):
#         if isSignal(signal, Signal.DetachMonsterZone, self.owner):
#             # 离场：扣回额外通常召唤次数（_reinitBuffAttr 已重置为1，此处确保不超出）
#             cur = self.game.normalSummonCntLimit[self.getSide()]
#             self.game.normalSummonCntLimit[self.getSide()] = max(1, cur - 1)
#             return
#
#         # 上场 或 每回合准备阶段（_reinitBuffAttr 重置后重新叠加）：额外通常召唤次数+1
#         if isSignal(signal, Signal.AttachMonsterZone, self.owner) or (
#             isSignal(signal, Signal.StandbyPhase)
#             and self.owner.isMonsterOnField()
#         ):
#             self.game.normalSummonCntLimit[self.getSide()] += 1
