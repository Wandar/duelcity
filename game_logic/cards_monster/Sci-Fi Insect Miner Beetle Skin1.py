# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Gyro Gear Grub
卡名:旋轮机虫
效果:1A:[把此卡解放]:抽1张卡;抽到机械族则再抽1张。
"""

class Sci_Fi_Insect_Miner_Beetle_Skin1(Card):
    CARD_KEY = 'Sci-Fi Insect Miner Beetle Skin1'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Sci_Fi_Insect_Miner_Beetle_Skin1_e1)


class Sci_Fi_Insect_Miner_Beetle_Skin1_e1(Effect):
    # 1A:[把此卡解放]:抽1张卡;抽到机械族则再抽1张。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.drawCard]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if len(self.game.decks[self.getSide()]) < 1:
            return False
        if justCheck:
            return True
        successNum = yield self.y_tributeCard(self.owner)
        if not successNum:
            return False
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        if len(self.game.decks[self.getSide()]) < 1:
            return False
        drawn = yield self.y_drawCard(self.getSide(), 1)
        if drawn and drawn[0].race == RACE.MACHINE and len(self.game.decks[self.getSide()]) > 0:
            yield self.y_drawCard(self.getSide(), 1)
        return True

