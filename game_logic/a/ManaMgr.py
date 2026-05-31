# -*- coding: utf-8 -*-
from __future__ import annotations
from KBEngine import *
from util import *
from npmath import *
from annos import *
from a.DuelConstants import *

class ManaMgr:
    def __init__(self, game):
        self.game:Game=game

        self.manaDatas:Dict[int, ManaData] = {}
        for i in game.monsters:
            m=ManaData()
            m.maxMana=0
            m.curMana=0
            m.maintenance=0
            self.manaDatas[i]=m

        self.manaPreUse=game.makeInitDict(0)


    def reserveMana(self, side, value):
        self.manaPreUse[side]+=value

    def cancelReserve(self,side,value):
        self.manaPreUse[side]-=value


    def affordableEffect(self,effect:Effect):
        if effect.manaCost==0:
            return True
        camp=effect.getSide()
        manaData=self.manaDatas[camp]
        if manaData.curMana-self.manaPreUse[camp]>=effect.manaCost:
            return True
        return False

    def affordable(self,side,manaCost):
        manaData=self.manaDatas[side]
        if manaData.curMana-self.manaPreUse[side]>=manaCost:
            return True
        return False

    def payManaCost(self,side,manaCost):
        manaData=self.manaDatas[side]
        manaData.curMana-=manaCost
        self._onManaChange()

    def payManaCostOfEffect(self,effect:Effect):
        camp=effect.getSide()
        manaData=self.manaDatas[camp]
        manaData.curMana-=effect.manaCost
        self._onManaChange()

    def recoverManaCostOfEffect(self,effect:Effect):
        camp=effect.getSide()
        manaData=self.manaDatas[camp]
        manaData.curMana+=effect.manaCost
        self._onManaChange()


    def _onManaChange(self):
        c_manas=self.game.duelNode.c_manas
        changed=False
        for camp,mana in self.manaDatas.items():
            if mana.__dict__!=c_manas[camp].__dict__:
                c_manas[camp]=ManaData(copy.copy(mana.__dict__))
                changed=True

        if changed:
            self.game.duelNode.c_manas=c_manas

    def recalMaintenance(self):
        pass


    #too many monsters with maintenance on field
    def y_checkManaOverMaintenance(self):
        for camp,manaData in self.manaDatas.items():
            if manaData.maintenance>manaData.maxMana:
                #TODO
                ERROR_MSG("manaData.maintenance>manaData.maxMana")

    #At the start of turn, player's locked mana crystals are removed.
    #Overloaded manas will becomes the newly locked mana.
    def onTurnStart(self):
        for camp,manaData in self.manaDatas.items():
            if camp==self.game.whoseTurn:
                if manaData.maxMana<5:
                    manaData.maxMana+=1
            manaData.curMana=manaData.maxMana-manaData.maintenance
        self._onManaChange()
