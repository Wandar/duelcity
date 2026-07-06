# -*- coding: utf-8 -*-
from __future__ import annotations

from util import *
from annos import *
from a.DuelConstants import *
from KBEngine import *

"""
aiChoice: popup / card-selector answering policy (moved verbatim in behavior
from the old botPack1.DuelAINormal).

Title classes decide the sort direction:
  harm_enemy   (destroy/banish/toGrave/bounce/steal/damage/target): pick the
               strongest enemy threat
  self_cost    (tribute/discard): pick the weakest (cheapest cost)
  self_benefit (search/special summon/fusion/equip/changeForm): pick the
               strongest / most useful
"""


def AI_MSG(*s):
    if True:
        DEBUG_MSG(*s)


class ChoiceMixin:
    """Mixin for DuelAINormal; relies on self.shouldWin / signatureMonstersPool /
    lowlevelMonsterPool / getSide / getEnemySideTuple / getBotConfig."""

    _HARM_ENEMY_TITLES = {
        TITLE.destroy, TITLE.banish, TITLE.sendToGrave,
        TITLE.returnToHand, TITLE.returnToDeck,
        TITLE.changeController, TITLE.damage, TITLE.target,
    }
    _SELF_COST_TITLES = {
        TITLE.tribute, TITLE.discard,
    }
    _SELF_BENEFIT_TITLES = {
        TITLE.addToHand, TITLE.specialSummon, TITLE.fusionSummon,
        TITLE.equip, TITLE.changeForm,
    }

    def _classifyTitle(self, title) -> str:
        if title in self._HARM_ENEMY_TITLES:
            return "harm_enemy"
        if title in self._SELF_COST_TITLES:
            return "self_cost"
        if title in self._SELF_BENEFIT_TITLES:
            return "self_benefit"
        return "neutral"

    def _scoreCard(self, card: Card, friendly: bool) -> float:
        """Score one card. friendly=True means the card is on our side.
        Higher = more valuable (worth keeping / bigger enemy threat)."""
        if card is None:
            return 0
        sig = self.signatureMonstersPool or []
        small = self.lowlevelMonsterPool or []

        try:
            base = float(card.getCurNumber())
        except Exception:
            base = 0.0

        # Signature monsters: ours = treasure, theirs = must answer
        if card.cardKey in sig:
            base += 5000

        # Own small fillers are nearly free to tribute / discard
        if friendly and card.cardKey in small:
            base -= 1000

        # Level weight: higher-level cards are better search targets
        base += card.level * 50

        # Position bonus
        try:
            if card.isOnField():
                base += 200
            elif card.isInHand():
                base += 100
        except Exception:
            pass

        # Enemy cards in defence are a discounted threat
        try:
            if not friendly and card.isDefence():
                base *= 0.7
        except Exception:
            pass

        return base

    def _pickByPolicy(self, title, cardList, minNum, maxNum, legalGroups):
        """Core selection policy; returns the picked card list."""
        mySide = self.getSide()
        enemySides = self.getEnemySideTuple()
        policy = self._classifyTitle(title)

        # --- 1. legalGroups present: score whole groups, take the best ---
        if legalGroups:
            def groupScore(g):
                total = sum(self._scoreCard(c, c.side == mySide) for c in g)
                if policy == "self_cost":
                    return -total          # cost: lower total value is better
                return total               # harm/benefit: higher is better
            best = max(legalGroups, key=groupScore)
            picked = list(best)
            if maxNum and len(picked) > maxNum:
                picked = picked[:maxNum]
            return picked

        if not cardList:
            return []

        # --- 2. plain list: sort by policy, slice ---
        def sortKey(c):
            friendly = (c.side == mySide)
            s = self._scoreCard(c, friendly)
            if policy == "self_cost":
                return s                    # ascending: weakest first
            if policy == "harm_enemy":
                bias = 10000 if c.side in enemySides else 0
                return -(s + bias)
            if policy == "self_benefit":
                bias = 10000 if friendly else 0
                return -(s + bias)
            return -s                       # neutral: most valuable first

        ordered = sorted(cardList, key=sortKey)

        # Benefit/harm: take as many as allowed; cost: bare minimum.
        if policy in ("self_benefit", "harm_enemy"):
            n = max(minNum, min(maxNum, len(ordered)))
        else:
            n = max(minNum, 1)
            n = min(n, maxNum if maxNum else n, len(ordered))
        return ordered[:n]

    # ============================================================
    # engine callbacks
    # ============================================================
    def y_onShowPopUp(self, title, text, options, defaultOption,
                      canCancel, popupType: POPUP_TYPE, reasonCard):
        yield WaitForSeconds(0.6)

        # Rock-paper-scissors: random
        if popupType == POPUP_TYPE.rockpaperscissors:
            return random.randint(0, 2)

        # Who goes first: win -> first, lose -> second
        if title == TITLE.decideWhoFirst:
            return 0 if self.shouldWin else 1

        # Activate an effect?
        if title == TITLE.shouldActivate:
            if not self.shouldWin:
                return 1                                    # losing: never activate
            sig = self.signatureMonstersPool or []
            if reasonCard is not None and reasonCard.cardKey in sig:
                return 0                                    # signature effects: always
            return defaultOption

        # Long text (chain choices): default
        if popupType == POPUP_TYPE.longText:
            return defaultOption

        # Generic YES/NO / askbattle: default (battle policy lives in the brain)
        return defaultOption

    def y_onShowCardSelectorPanel(self, title: str, options: [str], cardList: [Card],
                                  minNum=1, maxNum=1,
                                  defaultOption: int = 0, defaultResult: [Card] = DEFAULT_RESULT.random,
                                  canCancel=False, hasOrder=False,
                                  legalGroups: [[Card]] = None,
                                  otherSelected: Dict[int, Tuple[int, [Card], float]] = None
                                  ) -> Tuple[int, [Card]]:
        yield WaitForSeconds(0.6)

        # Nothing to choose from
        if not cardList and not legalGroups:
            return (defaultOption, [])

        # ---- losing: cancel when possible, else minimal legal answer ----
        if not self.shouldWin:
            if canCancel:
                return (1, [])                              # 1 = CANCEL
            if isinstance(defaultResult, list) and defaultResult:
                return (defaultOption, defaultResult)
            fallback = (cardList[:max(minNum, 1)] if cardList else [])
            return (defaultOption, fallback)

        # ---- winning: policy pick ----
        picked = self._pickByPolicy(title, cardList, minNum, maxNum, legalGroups)

        # Backfill up to minNum
        if len(picked) < minNum and cardList:
            rest = [c for c in cardList if c not in picked]
            picked = list(picked) + rest[:(minNum - len(picked))]

        AI_MSG("pickPolicy", title, "->", [c.cardKey for c in picked])
        return (defaultOption, picked)
