# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Breeze Sprite King
卡名:微风精灵王
效果:1P:自己其他风属性怪兽攻击力+200。2A:[把自己场上1只其他「微风」怪兽解放]:把对方场上1只攻击表示怪兽返回持有者手牌。
"""

class Wind_Mage(Card):
    CARD_KEY = 'Wind Mage'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Wind_Mage_e1)
        self.initEffect(Wind_Mage_e2)


class Wind_Mage_e1(Effect):
    # 1P:自己其他风属性怪兽攻击力+200。
    effType = EFF_TYPE.permanent
    observeSignals = (LOCATION.monsterZone, [Signal.AttachMonsterZone, Signal.DetachMonsterZone, Signal.CardAttrChanged])
    AI_HINT = [AI_HINT.permanent, AI_HINT.addAtk]
    EFF_POWER = 3

    def y_signal(self, signal):
        if isSignal(signal, Signal.DetachMonsterZone, self.owner):
            allCards = self.searchCards(LOCATION.mask_all, -1, CARD_TYPE.all, None)
            yield self.y_removeBuffEffectSource(allCards, self.effUniID)
            return
        if isSignal(signal, Signal.DetachMonsterZone):
            yield self.y_removeBuffEffectSource(signal.card, self.effUniID)
            return
        if not self.owner.isMonsterOnField():
            return
        def isOtherWind(c):
            return c != self.owner and c.attr == ATTR.WIND
        targets = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, None, isOtherWind)
        if targets:
            yield self.y_addCardData(targets, attackAdd=200,
                                     effDuration=EFF_DURATION.fromSource, uniqueSourceID=self.effUniID)


class Wind_Mage_e2(Effect):
    # 2A:[把自己场上1只其他「微风」怪兽解放]:把对方场上1只攻击表示怪兽返回持有者手牌。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.eraser, AI_HINT.costMonster]
    EFF_POWER = 3
    FAMILY = ("Whirlwind", "tinyWind", "Wind Mage")

    def y_cost(self, justCheck, signal):
        def isFodder(c):
            return c != self.owner and c.cardKey in self.FAMILY
        fodder = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, self, isFodder)
        if not fodder:
            return False
        def isAtk(c):
            return c.isFaceUp() and c.form == FORM.attack
        enemies = self.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(), CARD_TYPE.monster, self, isAtk)
        if not enemies:
            return False
        if justCheck:
            return True
        cost = yield self.y_select1Card(fodder, TITLE.tribute, canCancel=True)
        if not cost:
            return False
        target = yield self.y_select1Card(enemies, TITLE.returnToHand, canCancel=True)
        if not target:
            return False
        successNum = yield self.y_tributeCard(cost)
        if not successNum:
            return False
        self.saveTarget1(target)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1()
        if not t:
            return False
        yield self.y_returnCardToHand(t)
        return True

