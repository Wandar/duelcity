# -*- coding: utf-8 -*-
from __future__ import annotations
from dutil import *
from annos import *
"""
CardName:Crystal Ball
卡名:占卜水晶球
effect:
效果:1A:[最多使用3次][800LP]:猜测卡组顶端的卡的种类,猜对的情况将其加入手牌,猜错的情况将其覆盖到魔法陷阱区,然后破坏此卡
"""

class tmagicball(Card):
    CARD_KEY = "magicball"
    AUTHOR = "Unnamed"

    def effectsInit(self):
        self.initEffect(tmagicball_effect1)


class tmagicball_effect1(Effect):
    # 1A:[最多使用3次][800LP]:猜测卡组顶端的卡的种类,猜对加入手牌,猜错覆盖到魔法陷阱区并破坏此卡
    effType = EFF_TYPE.active
    countLimit = 3
    AI_HINT = [AI_HINT.drawCard]
    AI_POWER = 1

    def y_cost(self, justCheck, signal):
        if not self.getDeckLeftNum():
            return False
        if self.game.getPlayerLP(self.getSide()) <= 800:
            return False
        if justCheck:
            return True
        yield self.y_dealDamage(self.getSide(), 800)
        return True

    def y_activate(self, justCheck, signal):
        if justCheck:
            return True
        deck = self.game.decks[self.getSide()]
        if not deck:
            return False
        topCard = deck[-1]
        guessOption = yield self.y_onShowPopUp(
            TITLE.guess, "",
            [CARD_TYPE_STR.monster, CARD_TYPE_STR.spell, CARD_TYPE_STR.trap],
            0, False, POPUP_TYPE.normal, None)
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
            yield self.y_setCardToSpellZone(topCard)
            yield self.y_destroyCard(self.owner)
        return True
