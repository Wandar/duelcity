# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:magicball
卡名:magicball
"""
"""
1A:[最多使用3次][Cost:800LP]:猜测卡组顶端的卡的种类,猜对的情况将其加入手牌,猜错则返回卡组底部
"""
class tmagicball(Card):
    CARD_KEY="magicball"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(tmagicball_effect1)

class tmagicball_effect1(Effect):
    effType = EFF_TYPE.active

    countLimit = 3

    AI_HINT = [AI_HINT.drawCard]
    AI_POWER = 1

    def y_cost(self, justCheck:bool, signal):
        if not self.getDeckLeftNum():
            return False
        if self.game.getPlayerLP(self.getSide()) <= 800:
            return False
        if justCheck:
            return True
        yield self.y_dealDamage(self.getSide(), 800)
        return True

    def y_activate(self, justCheck:bool, signal):
        if justCheck:
            return True
        topCard = self.game.getTopDeckCard(self.getSide())
        if not topCard:
            return False
        # 让玩家猜测卡的种类
        guessOption = yield self.y_onShowPopUp(
            TITLE.guess, "",
            [CARD_TYPE_STR.monster, CARD_TYPE_STR.spell, CARD_TYPE_STR.trap],
            0, True, POPUP_TYPE.normal, None)
        correct = False
        if guessOption == 0 and (topCard.cardType & CARD_TYPE.monster):
            correct = True
        elif guessOption == 1 and (topCard.cardType & CARD_TYPE.spell):
            correct = True
        elif guessOption == 2 and (topCard.cardType & CARD_TYPE.trap):
            correct = True
        if correct:
            yield self.y_drawCard(self.getSide())
        else:
            yield self.y_sendCardToBottomDeck(topCard)
        return True
