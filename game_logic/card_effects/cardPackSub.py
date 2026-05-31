# -*- coding: utf-8 -*-
from __future__ import annotations
from annos import *
from KBEDebug import *
from a import Signal, fitter
from b.Card import *
from a.Effect import *
from a.DuelConstants import *
from Constants import *

try:
    from cards.specialsummon import *
    from cards.ripper import *
    from cards.search import *
    from cards.specialsummon import *
except:
    pass




class ghoul_boss(Card):
    CARD_KEY="ghoul_boss"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(ghoul_boss_effectSummon)

class ghoul_boss_effectSummon(Effect):
    effType = EFF_TYPE.active
    manaCost = 1

    activateLocation = LOCATION.monsterZone

    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 5

    def filter(self,card):
        if card.race!=RACE.UNDEAD:
            return False

        if card.level>4:
            return False

        if not card.canSpecialSummon():
            return False

    def y_activate(self,justCheck:bool,signal):
        cardList=self.game.searchCards(LOCATION.hand, self.getSide(), CARD_TYPE.monster, self.filter)

        if not len(cardList):
            return False

        if justCheck:
            return True

        card=yield self.game.y_select1Card(self.getSide(), TITLE.specialSummon, cardList)
        yield self.game.y_specialSummon(card)
        return True



"""
<手牌效果>:当你的LP在2000以下时,此卡特殊召唤
"""
class lowLPSummon(Effect):
    effType = EFF_TYPE.active

    activateLocation = LOCATION.hand

    AI_HINT = [AI_HINT.summonSelf]
    AI_POWER = 1
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        myLP=self.game.LPs[self.getSide()]
        if myLP>2000:
            return False

        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True

        yield self.y_specialSummon(self.owner)
        return True





"""
<战斗效果>:此卡战斗破坏对方怪兽后,从我方墓地特殊召唤一只LV4以下的怪兽
"""


"""
除外对方墓地的一只怪兽,然后特殊召唤我方墓地的一只LV6以下的怪兽
"""


"""
<被破坏时>:从卡组选2只LV4以下的怪兽特殊召唤
"""
