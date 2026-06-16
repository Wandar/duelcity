# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Caterpillar
卡名:毛毛虫
效果:1T:<对方回合结束时>:防御力+300。2A:<如果此卡防御力在2200以上>[献祭此卡]:从手牌把1只昆虫族怪兽特殊召唤。
"""

class Caterpillar(Card):
    CARD_KEY = 'Caterpillar'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(Caterpillar_e1)
        self.initEffect(Caterpillar_e2)


class Caterpillar_e1(Effect):
    # 1T:<对方回合结束时>:防御力+300。
    effType = EFF_TYPE.trigger
    observeSignals = (LOCATION.monsterZone, [Signal.TurnEnds])
    AI_HINT = [AI_HINT.enhance]
    EFF_POWER = 2
    countLimit = COUNT_LIMIT.unlimited

    def y_cost(self, justCheck, signal):
        if not isSignal(signal, Signal.TurnEnds):
            return False
        if self.game.whoseTurn == self.getSide():
            return False
        if not self.owner.isMonsterOnField():
            return False
        if justCheck:
            return True
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        yield self.y_addCardData(self.owner, defenceAdd=300, effDuration=EFF_DURATION.onceForever)
        return True


class Caterpillar_e2(Effect):
    # 2A:<如果此卡防御力在2200以上>[献祭此卡]:从手牌把1只昆虫族怪兽特殊召唤。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.summoner]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        if self.owner.defence < 2200:
            return False
        def isInsect(c):
            return c.race == RACE.INSECT
        targets = self.searchCards(LOCATION.hand, self.getSide(), CARD_TYPE.monster, self, isInsect)
        if not targets:
            return False
        if justCheck:
            return True
        chosen = yield self.y_select1Card(targets, TITLE.specialSummon, canCancel=True)
        if not chosen:
            return False
        successNum = yield self.y_tributeCard(self.owner)
        if not successNum:
            return False
        self.saveTarget1(chosen)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1()
        if not t or self.freeMonsterSpace() == 0:
            return False
        yield self.y_specialSummon(t)
        return True

