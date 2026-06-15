# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_undo  【陷阱】
卡图:绿色迷宫纹理背景,红色弧形撤销箭头,外圈黄色光晕,撤销回退。
效果(AOTIP):
1OT:<对方特殊召唤怪兽时>:时光倒带——把那只特殊召唤的怪兽返回持有者手卡;
   然后以自己墓地1张卡为对象,该卡加入手卡。
"""

class tT_Card_Ico_undo(Card):
    CARD_KEY = "T_Card_Ico_undo"
    AUTHOR = "Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_undo_eff)

class tT_Card_Ico_undo_eff(Effect):
    effType = EFF_TYPE.optionalInstant
    observeSignals = (LOCATION.spellTrapZone, [Signal.SpecialSummon])
    AI_HINT = [AI_HINT.eraser, AI_HINT.earn]
    EFF_POWER = 3

    def y_cost(self, justCheck: bool, signal):
        if not isSignal(signal, Signal.SpecialSummon): return False
        sumCard = signal.card
        if sumCard is None or sumCard.side not in self.getEnemySideTuple(): return False
        if not sumCard.isMonsterOnField(): return False
        if justCheck: return True
        self.saveTarget1(sumCard)
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck: return True
        t = self.getLegalTarget1()
        if t and t.isMonsterOnField():
            yield self.y_returnCardToHand(t, t.side_0)
        grave = self.searchCards(LOCATION.grave, self.getSide(), CARD_TYPE.all, self)
        if grave:
            g = yield self.y_select1Card(grave, TITLE.addToHand, self.getSide(), canCancel=True)
            if g:
                yield self.y_returnCardToHand(g, self.getSide())
        return True
