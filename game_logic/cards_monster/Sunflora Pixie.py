# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Sunlit Winged Sunflower King
卡名:向阳翼花王
效果:1T:<召唤时>:从弃牌区把最多2只「向阳翼花」怪兽以守备表示特殊召唤。
"""

class Sunflora_Pixie(Card):
    CARD_KEY = 'Sunflora Pixie'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Sunflora_Pixie_e1)


class Sunflora_Pixie_e1(Effect):
    # 1T:<召唤时>:从弃牌区把最多2只「向阳翼花」怪兽以守备表示特殊召唤。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.Summon])
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 4

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.Summon, self.owner):
            return False
        def isFamily(c):
            return c.cardKey in ("Sun Blossom", "Sunflower Fairy", "Sunflora Pixie")
        targets = self.searchCards(LOCATION.grave, self.getSide(), CARD_TYPE.monster, self, isFamily)
        if not targets:
            return False
        if self.freeMonsterSpace() == 0:
            return False
        if justCheck:
            return True
        maxn = min(2, self.freeMonsterSpace(), len(targets))
        chosen = yield self.y_selectCards(targets, TITLE.specialSummon, self.getSide(), 1, maxn, None, True)
        if not chosen:
            return False
        self.saveTarget1(chosen)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        targets = self.getLegalTarget1()
        if not targets:
            return False
        if type(targets) != list:
            targets = [targets]
        yield self.y_specialSummon(targets, form=FORM.defence)
        return True

