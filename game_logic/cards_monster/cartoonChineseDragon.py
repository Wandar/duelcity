# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Swirlthunder
卡名:漩漩雷云
效果:1A:把场上1只其他怪兽除外,下个回合的准备阶段将其返回原持有者场上。
"""

class cartoonChineseDragon(Card):
    CARD_KEY = 'cartoonChineseDragon'
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(cartoonChineseDragon_e1)


class cartoonChineseDragon_e1(Effect):
    # 1A:把场上1只其他怪兽除外,下个回合的准备阶段将其返回原持有者场上。
    # NOTE: 暂无"延迟返回"调度钩子,这里实现为除外;返回部分留待引擎支持延迟效果。
    effType = EFF_TYPE.active
    activateLocation = LOCATION.monsterZone
    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 3

    def y_cost(self, justCheck, signal):
        def isOther(c):
            return c != self.owner
        targets = self.searchCards(LOCATION.monsterZone, -1, CARD_TYPE.monster, self, isOther)
        if not targets:
            return False
        if justCheck:
            return True
        t = yield self.y_select1Card(targets, TITLE.banish, canCancel=True)
        if not t:
            return False
        self.saveTarget1(t)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        t = self.getLegalTarget1()
        if not t:
            return False
        yield self.y_banishCard(t)
        return True

