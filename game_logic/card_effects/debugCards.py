# -*- coding: utf-8 -*-
from __future__ import annotations
from annos import *
from KBEDebug import *
from a import Signal, fitter
from b.Card import *
from a.Effect import *
from a.DuelConstants import *
from Constants import *
#
# DEBUGCARD_AAA_DATA = {
#     "key": "dragonDCard",  #unique,must not conflict with the "key" tags in ALL_DATA.json and in this file
#     "name_en": "Fire Dragon",
#     "name_zh": "大火龙",
#     "type": "MONSTER",
#     "image":"",
#     "prefab": "dame",  #decide the appearance of this unit,You can use the "key" tag from ALL_DATA.json
#     "package": "dame", #normally same as prefab
#     "diameter": 3.0,  #how big is this unit
#     "attack": 1,
#     "defense": 1,
#     "health": 1,
#     "attr": 0,
#     "level": 1,
#     "race": 0,
#     "short_effects": "", #short effects
#     "effect_en": "", #just text
#     "effect_zh": "",
# }
#
#
# class DebugCardAAA:
#     CARD_DATA = DEBUGCARD_AAA_DATA  #comment this line to exclude from merge
#
#     def __init__(self):
#         pass

# class zenyuan(Spell):
#     KEY="zenyuan"
#     def createEffectAttr(self):
#         pass
#
#     def y_cost(self):
#         pass
#
#     def y_activate(self):
#         allCards=chooseDeck
#
#         result=yield self.duel.y_showCardSelect()
#         result.sendToHand()
#
#
# #选择效果1和2
# class zenyuan(Spell):
#     KEY="zenyuan"
#     def createEffectAttr(self):
#         pass
#
#     #选择哪一个
#     def y_chooseWhich(self):
#         pass
#
#     def y_cost(self):
#         pass
#
#     def y_activate(self):
#         allCards=chooseDeck
#
#         result=yield self.duel.y_showCardSelect()
#         result.sendToHand()
#
#     def y_cost1(self):
#         pass
#
#     def y_activate1(self):
#         pass




class ACS17(Card):
    # CARD_KEY="ACS17"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(ACS17_effect1)

"""
释放场上的一只怪兽,对对手场上的一只怪兽造成3点伤害
"""
class ACS17_effect1(Effect):
    effType = EFF_TYPE.active

    observeSignals = (LOCATION.monsterZone,[Signal.NormalSummon])

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 1
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        monsters=self.searchCards(LOCATION.monsterZone,self.getSide(),CARD_TYPE.monster,self)

        if not monsters:
            return False

        if justCheck:
            return True

        monster=yield self.y_select1Card(monsters,TITLE.tribute,canCancel=True)
        if not monster:
            return False
        success=yield self.y_tributeCard(monster)
        if not success:
            return False

        return True

    def y_activate(self,justCheck:bool,signal):
        enMonsters=self.searchCards(LOCATION.monsterZone,self.getEnemySideTuple(),CARD_TYPE.monster,self)
        if not enMonsters:
            return False

        if justCheck:
            return True

        monster=yield self.y_select1Card(enMonsters,TITLE.target)
        yield self.y_damageCard(monster,3)
        return True