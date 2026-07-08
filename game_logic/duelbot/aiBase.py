# -*- coding: utf-8 -*-
from __future__ import annotations

from util import *
from annos import *
from a.DuelConstants import *
from KBEngine import *

"""
aiBase: engine-facing plumbing shared by all duel AIs.

DuelAIBase wires the engine callbacks (onTick / onDuelStart / popup defaults)
and runs the main loop: call y_think() repeatedly until it reports "nothing
more to do", then end the turn. No strategy lives here — strategy is
y_think() in aiBrain.py.
"""


def AI_MSG(*s):
    if True:
        DEBUG_MSG(*s)


# Hard cap of think steps per turn (protects against decision loops)
MAX_MOVES_PER_TURN = 30


class DuelAIBase(Reload):
    avatar: AvatarCE = None
    duel: Duel = None
    game: Game

    def __init__(self, avatar):
        Reload.__init__(self, True, False)
        self.avatar = avatar

    def getSide(self):
        return self.avatar.c_side

    def getEnemySideTuple(self) -> Tuple[int]:
        return self.duel.getEnemySideTuple(self.getSide())

    def getAllySideTuple(self) -> Tuple[int]:
        return self.duel.getAllySideTuple(self.getSide())

    def onDuelStart(self, duel):
        self.duel = duel
        self.game = duel.game

    def onTurnStart(self):
        pass

    # Normal summon "like a player": sets game.playerop around the call so the
    # bot avatar plays AVATAR_ANIM.summon (see the playerop gate in
    # GameFunc.y_normalSummon). Use this instead of game.y_normalSummon for
    # every summon the bot performs as if it clicked the card itself.
    def y_playerlikeNormalSummon(self, card, toWhoseSide=0, costNormalSummonChance=True, tributeNumChange=None):
        game = self.game
        game.playerop = (card.side, OPERATE.normalSummon)
        ok = yield game.y_normalSummon(False, card, toWhoseSide, costNormalSummonChance, tributeNumChange)
        game.playerop = (0, 0)
        return ok

    # Async init right after duel start (e.g. request win/lose from player base). Default: no-op.
    def y_initDuelAI(self):
        yield None

    def onDuelEnd(self, duel):
        pass

    def y_signal(self, signal):
        pass

    # ------------------------------------------------------------
    # Popup / selector defaults (overridden by ChoiceMixin in aiChoice.py)
    # ------------------------------------------------------------
    def y_onShowPopUp(self, title: str, text: str, options: [str], defaultOption: int,
                      canCancel: bool, popupType: POPUP_TYPE, reasonCard) -> int:
        yield WaitForSeconds(0.6)
        return defaultOption

    def y_onShowCardSelectorPanel(self, title: TITLE, options: [str], cardList: [Card],
                                  minNum: int, maxNum: int, defaultOption: int,
                                  defaultResult: [Card], canCancel: bool, hasOrder: bool,
                                  legalGroups: [[Card]],
                                  otherSelected: Dict[int, Tuple[int, [Card], float]]) -> Tuple[int, [Card]]:
        if not defaultResult:
            defaultResult = []
        yield WaitForSeconds(0.6)
        return (defaultOption, defaultResult)

    def y_arrangeTriggerEffects(self, queue: List[Effect]) -> List[Effect]:
        return queue

    def y_selectInstantEffect(self, queue: List[Effect]) -> Effect:
        if len(queue):
            return queue[0]
        return None

    # ------------------------------------------------------------
    # Engine tick: start the main loop coroutine on our own turn
    # ------------------------------------------------------------
    def onTick(self):
        selfside = self.avatar.c_side
        duel = self.duel = self.avatar.getDuel()
        if not duel or not duel.game:
            return
        if duel.hasLoser():
            return
        if duel.stage != DUEL_STAGE.dueling:
            return
        if duel.game.whoseTurn != selfside:
            return

        duelNode = duel.duelNode
        if not duelNode.hasCoroutine("y_bot_operateRepeat"):
            duelNode.startCoroutine(self.y_bot_operateRepeat(), False, 0)

    # ------------------------------------------------------------
    # Main loop: y_think() does one check-then-act step and returns True
    # while it keeps making progress; False (or the step cap) ends the turn.
    # ------------------------------------------------------------
    turnWaitedAtStart = False

    def y_bot_operateRepeat(self):
        game = self.game
        INFO_MSG("start bot ai, turn=", game.curTurn)

        if not self.turnWaitedAtStart:
            self.turnWaitedAtStart = True
            #4s: give the client time to finish the draw-card animation
            #before the bot starts acting
            yield WaitForSeconds(4)

        for _ in range(MAX_MOVES_PER_TURN):
            acted = yield self.y_think()
            if not acted:
                break
            yield WaitForSeconds(random.uniform(0.5, 1.0))

        yield game.y_turnEnds()

    # ---- abstract: one decision step, implemented in aiBrain ----
    def y_think(self):
        yield None
        return False
