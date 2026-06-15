# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:T_Card_Ico_charge_battery  【永续魔法】
卡图:蓝色背景,绿色电池中心黄色闪电标志,四周迸出闪电,充能蓄力。
效果(AOTIP):
1A:[每回合1次]:充能——在此卡上放置1个电量计数器(最多5个)。
2A:[每回合1次]:放电——以自己场上1只怪兽为对象,这个回合其{ATK}上升 电量×500,然后移除全部电量。
"""

class tT_Card_Ico_charge_battery(Card):
    CARD_KEY = "T_Card_Ico_charge_battery"
    AUTHOR = "Unnamed"
    def effectsInit(self):
        self.initEffect(tT_Card_Ico_charge_battery_charge)
        self.initEffect(tT_Card_Ico_charge_battery_discharge)

class tT_Card_Ico_charge_battery_charge(Effect):
    effType = EFF_TYPE.active
    activateLocation = LOCATION.spellTrapZone
    countLimit = COUNT_LIMIT.oncePerTurn
    AI_HINT = [AI_HINT.enhance]
    EFF_POWER = 1

    def y_cost(self, justCheck: bool, signal):
        if not self.owner.isInSpellZone(): return False
        if int(self.owner.getData("battery") or 0) >= 5: return False
        if justCheck: return True
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck: return True
        self.owner.setData("battery", min(5, int(self.owner.getData("battery") or 0) + 1))
        return True
        yield

class tT_Card_Ico_charge_battery_discharge(Effect):
    effType = EFF_TYPE.active
    activateLocation = LOCATION.spellTrapZone
    countLimit = COUNT_LIMIT.oncePerTurn
    AI_HINT = [AI_HINT.addAtk]
    EFF_POWER = 3

    def y_cost(self, justCheck: bool, signal):
        if int(self.owner.getData("battery") or 0) <= 0: return False
        myMons = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self)
        if not myMons: return False
        if justCheck: return True
        t = yield self.y_select1Card(myMons, TITLE.target, self.getSide(), canCancel=True)
        if not t: return False
        self.saveTarget1(t)
        return True

    def y_activate(self, justCheck: bool, signal):
        if justCheck: return True
        n = int(self.owner.getData("battery") or 0)
        self.owner.setData("battery", 0)
        t = self.getLegalTarget1()
        if t and t.isMonsterOnField() and n > 0:
            yield self.y_addCardData(t, attackAdd=n*500,
                                     effDuration=EFF_DURATION.utilTurnEnds, uniqueSourceID=self.effUniID)
        return True
