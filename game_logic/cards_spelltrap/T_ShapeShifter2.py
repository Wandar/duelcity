# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_ShapeShifter2  【魔法】
卡图:深蓝背景,一张脸左半人类右半黑色狼头露尖牙,绿色旋转烟雾,变形者两面形态。
效果(AOTIP):
1A:以自己场上1只怪兽和场上另1只怪兽为对象,这个回合中自己的那只怪兽的
   {ATK}/{DEF}/星级/属性/种族变为与另1只相同(变形)。
"""

class tT_ShapeShifter2(Card):
    CARD_KEY = "T_ShapeShifter2"
    AUTHOR = "Unnamed"
    def effectsInit(self):
        self.initEffect(tT_ShapeShifter2_eff)

class tT_ShapeShifter2_eff(Effect):
    effType = EFF_TYPE.active
    activateLocation = LOCATION.spellTrapZone
    AI_HINT = [AI_HINT.enhance]
    EFF_POWER = 3

    def y_cost(self, justCheck: bool, signal):
        myMons = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self)
        allMons = self.searchCards(LOCATION.monsterZone, -1, CARD_TYPE.monster, self)
        if not myMons or len(allMons) < 2: return False
        if justCheck: return True
        shifter = yield self.y_select1Card(myMons, TITLE.target, self.getSide(), canCancel=True)
        if not shifter: return False
        templates = [c for c in allMons if c is not shifter]
        if not templates: return False
        tpl = yield self.y_select1Card(templates, TITLE.target, self.getSide(), canCancel=True)
        if not tpl: return False
        self.saveTarget1(shifter)
        self.saveTarget2(tpl)
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck: return True
        shifter = self.getLegalTarget1()
        tpl = self.getLegalTarget2()
        if shifter and tpl and shifter.isMonsterOnField() and tpl.isMonsterOnField():
            yield self.y_changeCardData(shifter, newAtk=tpl.atk, newDefence=tpl.defence,
                                        newLevel=tpl.level, newAttr=tpl.attr, newRace=tpl.race,
                                        effDuration=EFF_DURATION.utilTurnEnds, uniqueSourceID=self.effUniID)
        return True
