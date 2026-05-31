# -*- coding: utf-8 -*-
from __future__ import annotations
from util import *
from a.DuelConstants import *
from annos import *


g_playerBuffClasses={} #{1:}


class PlayerBuff:
    _IS_PLAYER_BUFF=True

    BUFF_ID:PLAYER_BUFF = 0
    FX= FX_ID.none

    side=0
    addTurn=0

    duration:EFF_DURATION=EFF_DURATION.onceForever
    sourceID=0

    def __init__(self,duration,sourceID):
        self.duration=duration
        self.sourceID=sourceID

    def onBuff(self,game:Game):
        pass


class cantDeclareAttack(PlayerBuff):
    pass

class cantDirectAttack(PlayerBuff):
    pass

class cardBanishedInsteadIntoGrave(PlayerBuff):
    pass


