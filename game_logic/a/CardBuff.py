# -*- coding: utf-8 -*-
from __future__ import annotations

import math
from KBEDebug import *
from a.DuelConstants import *
from annos import *
if 0:
    from b.Card import Card

from util import *
from Constants import *


g_buffClasses={} #{1:}


class CardBuff:
    _IS_CARD_BUFF=True

    IS_CHANGE_TO=False
    TYPE=""

    BUFF_ID = 0
    fxID=FX_ID.none

    owner:Card=None
    addTurn=0

    duration:EFF_DURATION=EFF_DURATION.onceForever
    uniqueSourceID=0

    def __init__(self, duration=EFF_DURATION.onceForever, uniqueSourceID=0):
        # CardBuffData.__init__(self,None)
        # self.uniID=owner.game.genUniID()

        self.duration=duration
        self.uniqueSourceID=uniqueSourceID

    def onBuff(self,card):
        pass


class attackChange(CardBuff):
    number=0
    IS_CHANGE_TO = True
    TYPE="attack"
    def onBuff(self,card : Card):
        card.atk=int(self.number)
        card.atk=limit(card.atk,0,2147483647)


class rangeAtkChange(CardBuff):
    number=0
    IS_CHANGE_TO = True
    TYPE="range"
    def onBuff(self,card : Card):
        if card.rangeAtk!=ATK.none:
            card.rangeAtk=int(self.number)
            card.rangeAtk=limit(card.rangeAtk,0,60000)


class defenceChange(CardBuff):
    number=0
    IS_CHANGE_TO = True
    TYPE="defence"
    def onBuff(self,card : Card):
        card.defence=int(self.number)
        card.defence=limit(card.defence,0,2147483647)


class attackAdd(CardBuff):
    number=0
    TYPE="attack"
    def onBuff(self,card : Card):
        card.atk+=self.number
        card.atk=int(card.atk)
        card.atk=limit(card.atk,0,2147483647)


class rangeAtkAdd(CardBuff):
    number=0
    TYPE="range"
    def onBuff(self,card : Card):
        if card.rangeAtk!=ATK.none:
            card.rangeAtk+=self.number
            card.rangeAtk=limit(card.rangeAtk,0,60000)


class defenceAdd(CardBuff):
    number=0
    TYPE="defence"
    def onBuff(self,card : Card):
        card.defence+=int(self.number)
        card.defence=limit(card.defence,0,2147483647)


class attackMulti(CardBuff):
    number=0
    TYPE="attack"
    def onBuff(self,card : Card):
        card.atk*=self.number
        card.atk=limit(card.atk,0,2147483647)


class rangeAtkMulti(CardBuff):
    number=0
    TYPE="range"
    def onBuff(self,card : Card):
        if card.rangeAtk!=ATK.none:
            card.rangeAtk*=self.number
            card.rangeAtk=limit(card.rangeAtk,0,60000)


class defenceMulti(CardBuff):
    number=0
    TYPE="defence"
    def onBuff(self,card : Card):
        card.defence*=self.number
        card.defence=limit(card.defence,0,2147483647)


class levelChange(CardBuff):
    number=0
    IS_CHANGE_TO = True
    TYPE="level"
    def onBuff(self,card:Card):
        card.level=self.number
        card.level=limit(card.level,0,127)


class levelAdd(CardBuff):
    number=0
    TYPE="level"
    def onBuff(self,card : Card):
        card.level+=self.number
        card.level=limit(card.level,0,127)


class attackTimesChange(CardBuff):
    number=0
    IS_CHANGE_TO = True
    TYPE="attackTimes"
    def onBuff(self,card:Card):
        card.attackCntLimitPerTurn=self.number


class attackTimesAdd(CardBuff):
    number=0
    TYPE="attackTimes"
    def onBuff(self,card : Card):
        card.attackCntLimitPerTurn+=self.number


class attrChange(CardBuff):
    newAttr=ATTR.DARK
    IS_CHANGE_TO = True
    def onBuff(self,card:Card):
        card.attr=self.newAttr

class raceChange(CardBuff):
    newRace=RACE.WARRIOR
    IS_CHANGE_TO = True
    def onBuff(self,card:Card):
        card.race=self.newRace


class controlled(CardBuff):
    pass

#TODO
class immunity(CardBuff):
    immunityMask:IMMUNITY_MASK=IMMUNITY_MASK.effectDamage|IMMUNITY_MASK.battleDamage
    def onBuff(self,card):
        card.immunityMask|=self.immunityMask

class silenced(CardBuff):
    fxID = FX_ID.silenced
    def onBuff(self,card):
        card.isSilenced=True

class voided(CardBuff):
    pass

class temporary(CardBuff):
    pass
