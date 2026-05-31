# -*- coding: utf-8 -*-
from __future__ import annotations

from KBEngine import *

from util import *
from annos import *


def __________________________1cardFilter():
    pass


def canTribute(reasonCard,card:Card):
    if card.isMonster() and card.canTribute(reasonCard):
        return True
    return False

def canDestroy(reasonCard,card:Card):
    if card.canDestroy():
        return False

def filterRaceAndLVLimit(race,levelLimit,card):
    if card.race!=race:
        return False
    if card.level>levelLimit:
        return False
    return True


def filterCanBeDestroy(card:Card):
    if card.canDestroy():
        return True
    return False


def ___________________________groupFilter():
    pass

def groupCanNormalSummonTribute(reasonCard:Card,cardList:[Card]):
    allPoint=reasonCard.getNormalSummonTributeNum()
    cnt=0
    for card in cardList:
        cnt+=card.getTributePoint(SUMMON_TYPE.normalSummon,reasonCard)
    if cnt==allPoint:
        return True
    return False



def extraSummonLevelLimit(level, cardList):
    return sum(card.level for card in cardList)==level


def extraSummonFromExtraDeckFilter(reasonCard:Card, cardList:[Card]):
    level=reasonCard.level

    if len(cardList)<2:
        return False

    #check tuner
    for i in range(len(cardList)):
        card=cardList[i]
        if i==0:
            if card.isOrangeNamedMonster():
                pass
            else:
                return False
        else:
            if card.isOrangeNamedMonster():
                return False

    #check level
    if sum(card.level for card in cardList)!=level:
        return False

    return True




def ______________________________________finder():
    pass


def getTheMostPowerfulMonster(cardList:[Card]):
    max_level = max(cardList, key=lambda x: x.level).level
    max_level_cards = [card for card in cardList if card.level == max_level]
    max_hp_card = max(max_level_cards, key=lambda x: x.hp)
    return max_hp_card