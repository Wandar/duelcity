# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:104snowmonster
卡名:104snowmonster
"""

"""
1A:破坏自己场上一只的LV6以上的怪兽,然后破坏对方两张魔法陷阱卡
"""

class t104snowmonster(Card):
    CARD_KEY="104snowmonster"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(t104snowmonster_effect1)

class t104snowmonster_effect1(Effect):
    effType = EFF_TYPE.active

    AI_HINT = [AI_HINT.eraser]
    AI_POWER = 1
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        enemySpells=self.searchCards(LOCATION.spellTrapZone,self.getEnemySideTuple(),CARD_TYPE.all,self)
        if not enemySpells:
            return

        myLV6=self.searchCards(LOCATION.monsterZone,0,CARD_TYPE.monster,self,lambda card:card.level>=6)
        if not myLV6:
            return

        if justCheck:
            return True

        target=yield self.y_select1Card(myLV6,TITLE.destroy,canCancel=True)
        enemySpellsToDestroy=yield self.y_selectCards(enemySpells,TITLE.destroy,0,1,2,canCancel=True)
        if target and enemySpellsToDestroy:
            self.saveTarget1(target)
            self.saveTarget2(enemySpellsToDestroy)
            return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True

        target=self.getLegalTarget1()
        snum=yield self.y_destroyCard(target)
        if snum==0:
            return
        target2=self.getLegalTarget2()
        yield self.y_destroyCard(target2)
