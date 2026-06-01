# -*- coding: utf-8 -*-
from __future__ import annotations
from KBEDebug import *
from a import Signal, fitter
from b.Card import *
from a.Effect import *
from a.DuelConstants import *
from Constants import *


ENGINE_VERSION=1
D_SCRIPT_VERSION=1


def getMonsterOnFieldWithHighestAtk(game:Game):
    monsterList=game.searchCards(LOCATION.monsterZone)
    if not len(monsterList):
        return None


def compareCardAtk(a:Card,b:Card):
    pass




def isEnemyHasMoreMonster(game,side):
    pass

def defaultMonsterToAttack():
    pass


def listGetHighestHPMonster(cardList)->Card:
    pass

def listContainMonsterWithLV(cardList)->bool:
    pass

def listContainMonsterWithHP(cardList)->bool:
    pass

def listGetDangerousMonster(cardList)->List[Card]:
    pass

