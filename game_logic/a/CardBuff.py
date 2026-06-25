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


class ShortEffectBuff(CardBuff):
    """
    Carries a runtime-granted short effect. The buff itself only rides the duration
    machinery (turn-end / battle-end sweeps, remove-by-source); the actual Effect
    instance is created and torn down by Card._recalBuffs reconciliation, so a
    granted short effect disappears exactly like a buff when this buff expires.
    """
    BUFF_ID = CARD_BUFF.shortEffectAdd

    def __init__(self, shortEffectName="", data="",
                 duration=EFF_DURATION.onceForever, uniqueSourceID=0):
        CardBuff.__init__(self, duration, uniqueSourceID)
        self.shortEffectName = shortEffectName
        # single carrier for any number/data; the granted effect reads it via
        # getShortEffectTailNumber() (int(self.data)) just like static short effects
        self.data = data

    def onBuff(self, card):
        # connection is handled by Card._recalBuffs reconciliation, not here
        pass


# NOTE: stat buffs apply WITHOUT clamping here. Card._recalBuffs clamps once after every
# buff is applied, so a large reduction followed by an addition lands on the true sum
# instead of being lost at 0 mid-way.
class attackChange(CardBuff):
    number=0
    IS_CHANGE_TO = True
    TYPE="attack"
    def onBuff(self,card : Card):
        card.atk=int(self.number)


class rangeAtkChange(CardBuff):
    number=0
    IS_CHANGE_TO = True
    TYPE="range"
    def onBuff(self,card : Card):
        if card.rangeAtk!=ATK.none:
            card.rangeAtk=int(self.number)


class defenceChange(CardBuff):
    number=0
    IS_CHANGE_TO = True
    TYPE="defence"
    def onBuff(self,card : Card):
        card.defence=int(self.number)


class attackAdd(CardBuff):
    number=0
    TYPE="attack"
    def onBuff(self,card : Card):
        card.atk+=self.number


class rangeAtkAdd(CardBuff):
    number=0
    TYPE="range"
    def onBuff(self,card : Card):
        if card.rangeAtk!=ATK.none:
            card.rangeAtk+=self.number


class defenceAdd(CardBuff):
    number=0
    TYPE="defence"
    def onBuff(self,card : Card):
        card.defence+=self.number


class attackMulti(CardBuff):
    number=0
    TYPE="attack"
    def onBuff(self,card : Card):
        card.atk*=self.number


class rangeAtkMulti(CardBuff):
    number=0
    TYPE="range"
    def onBuff(self,card : Card):
        if card.rangeAtk!=ATK.none:
            card.rangeAtk*=self.number


class defenceMulti(CardBuff):
    number=0
    TYPE="defence"
    def onBuff(self,card : Card):
        card.defence*=self.number


class levelChange(CardBuff):
    number=0
    IS_CHANGE_TO = True
    TYPE="level"
    def onBuff(self,card:Card):
        card.level=self.number


class levelAdd(CardBuff):
    number=0
    TYPE="level"
    def onBuff(self,card : Card):
        card.level+=self.number


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

class immunity(CardBuff):
    immunityMask:IMMUNITY_MASK=IMMUNITY_MASK.damage
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
