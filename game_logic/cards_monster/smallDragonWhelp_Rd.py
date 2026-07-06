# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Lava Hatchling Dragon
卡名:熔岩雏龙
效果:1T:<此卡被特殊召唤时>:发现一张龙族怪兽并守备召唤。
"""

class smallDragonWhelp_Rd(Card):
    CARD_KEY = 'smallDragonWhelp_Rd'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(smallDragonWhelp_Rd_e1)


class smallDragonWhelp_Rd_e1(Effect):
    # 1T:<此卡被特殊召唤时>:发现一张龙族怪兽并守备召唤。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.SpecialSummon])
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 4

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.SpecialSummon, self.owner):
            return False
        if self.freeMonsterSpace() == 0:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        picked = yield self.y_discoverCard(side=self.getSide(), race=RACE.DRAGON,
                                           cardType=CARD_TYPE.monster, count=3, title=TITLE.specialSummon, canCancel=True)
        if picked and self.freeMonsterSpace() > 0:
            yield self.y_specialSummon(picked, form=FORM.defence)
        return True
