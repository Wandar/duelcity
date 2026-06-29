# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Mechanical Velociraptor
卡名:机器速龙
效果:1A:[把此卡解放]:从卡组·弃牌区把最多2只等级4以下的机械族怪兽临时召唤。2P:我方场上其他机械族怪兽攻击力·守备力上升300。
"""

class SK_VelociraptorMech(Card):
    CARD_KEY = 'SK_VelociraptorMech'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(SK_VelociraptorMech_e1)
        self.initEffect(SK_VelociraptorMech_e2)


class SK_VelociraptorMech_e1(Effect):
    # 1A:[把此卡解放]:从卡组·弃牌区把最多2只等级4以下的机械族怪兽临时召唤(回合结束时送墓)。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.summoner, AI_HINT.costMonster]
    EFF_POWER = 4

    def y_cost(self, justCheck, signal):
        if not self.owner.isMonsterOnField():
            return False
        def isT(c):
            return c != self.owner and c.race == RACE.MACHINE and c.level <= 4
        targets = self.searchCards(LOCATION.deck | LOCATION.grave, self.getSide(), CARD_TYPE.monster, self, isT)
        if not targets:
            return False
        if self.freeMonsterSpace() < 1:
            return False
        if justCheck:
            return True
        maxNum = min(2, self.freeMonsterSpace(), len(targets))
        chosen = yield self.y_selectCards(targets, TITLE.specialSummon, self.getSide(), 1, maxNum, None, True)
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
        targets = self._getLegalTargetList1(False)
        if not targets:
            return False
        yield self.y_specialSummon(list(targets), buffIDOrList=CARD_BUFF.temporary)
        return True


class SK_VelociraptorMech_e2(Effect):
    # 2P:我方场上其他机械族怪兽攻击力·守备力上升300。
    effType = EFF_TYPE.permanent
    observeSignals = (LOCATION.monsterZone, [Signal.AttachMonsterZone, Signal.DetachMonsterZone, Signal.CardRaceChanged])
    AI_HINT = [AI_HINT.permanent, AI_HINT.enhance]
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
        def isOtherMachine(c):
            return c != self.owner and c.race == RACE.MACHINE
        targets = self.searchCards(LOCATION.monsterZone, self.getSide(), CARD_TYPE.monster, None, isOtherMachine)
        if targets:
            yield self.y_addCardData(targets, attackAdd=300, defenceAdd=300,
                                     effDuration=EFF_DURATION.fromSource, uniqueSourceID=self.effUniID)
