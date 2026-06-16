# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Mecha Blood Mosquito
卡名:机械吸血蚊
效果:1T:<战斗破坏对方怪兽时>:自己抽1张卡。
"""

class Sci_Fi_Insect_Mosquito_Skin2(Card):
    CARD_KEY = 'Sci-Fi Insect Mosquito Skin2'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Sci_Fi_Insect_Mosquito_Skin2_e1)


class Sci_Fi_Insect_Mosquito_Skin2_e1(Effect):
    # 1T:<战斗破坏对方怪兽时>:自己抽1张卡。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.BattleFinish])
    AI_HINT = [AI_HINT.drawCard]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.BattleFinish):
            return False
        if signal.attackerCard != self.owner:
            return False
        rc = signal.receiverCard
        if rc is None or rc.isMonsterOnField():
            return False
        if len(self.game.decks[self.getSide()]) < 1:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        yield self.y_drawCard(self.getSide(), 1)
        return True

