# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_shadow_hand
卡名:阴影之手
"""

#########################my

"""
1I:对方发动效果时,随机查看对方1张手牌,若为怪兽使该效果无效
"""

class tT_Card_Ico_shadow_hand(Card):
    CARD_KEY="T_Card_Ico_shadow_hand"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_shadow_hand_effect1)

class tT_Card_Ico_shadow_hand_effect1(Effect):
    effType = EFF_TYPE.optionalInstant

    observeSignals = (LOCATION.spellTrapZone, [Signal.BeforeActivateEffect])

    AI_HINT = [AI_HINT.eraser]
    AI_POWER = 1

    enemy=0
    def y_cost(self, justCheck:bool, signal):
        if not isSignal(signal, Signal.BeforeActivateEffect):
            return
        srcCard = getattr(signal, 'sourceCard', None)
        if not srcCard or srcCard.side not in self.getEnemySideTuple():
            return

        if justCheck:
            return True

        self.enemy = yield self.y_select1EnemySide()
        if not self.game.hands[self.enemy]:
            return
        return True

    def y_activate(self, justCheck:bool, signal:Signal.BeforeActivateEffect):
        if justCheck:
            return True
        import random
        enemy=self.enemy
        hand = self.game.hands[enemy]
        if not hand:
            return
        peek = random.choice(hand)
        # pseudo: reveal the peeked card to controller briefly
        yield self.y_revealCardToSide(peek, self.getSide())
        if peek.cardType & CARD_TYPE.monster:
            yield self.y_counterEffectActivate(signal)
