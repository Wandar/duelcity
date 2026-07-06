# -*- coding: utf-8 -*-
from __future__ import annotations

from util import *
from annos import *
from a.DuelConstants import *
from KBEngine import *

"""
aiCombos: one combo = one ComboBase subclass in this file. The registry is
built automatically by scanning the module — defining the class IS the
registration, no manual COMBOS entry needed.

Class layout:
  - class attributes = the combo's config (need keys, space requirements...)
  - y_combo(bot, justCheck): staticmethod following the project's
    y_normalSummon(justCheck, ...) convention:
      justCheck=True  -> return the list of missing cardKeys before any yield:
                           []            = ready, can run right now
                           [key, ...]    = cards missing from hand (supply-fixable)
                           contains None = not runnable this turn (summon count /
                                           space / phase...), the supply can't help
      justCheck=False -> play the combo using REAL hand cards only, through
                         the normal game APIs; return True/False for success.

Combos never create cards. If cards are missing, the brain first calls
supply.provideToHand (CardSupply morphs hidden hand cards), then the combo
checks ready on the next think step and plays itself.
"""


def AI_MSG(*s):
    if True:
        DEBUG_MSG(*s)


class ComboBase:
    """Base of all combos. Subclass, set config as class attributes and
    implement y_combo; the registry picks the subclass up automatically."""

    NAME = ""  # registry key; empty = class name with the "Combo_" prefix stripped

    @classmethod
    def getName(cls):
        if cls.NAME:
            return cls.NAME
        name = cls.__name__
        if name.startswith("Combo_"):
            return name[len("Combo_"):]
        return name

    @staticmethod
    def y_combo(bot, justCheck):
        raise NotImplementedError


class ComboPlan:
    """Result of evaluating one not-yet-ready combo."""

    def __init__(self, name, missing):
        self.name = name
        self.missing = missing

    def __repr__(self):
        return "ComboPlan(%s missing=%s)" % (self.name, self.missing)


def runJustCheck(comboCls, bot):
    """Drive a combo's y_combo synchronously in justCheck mode.

    The justCheck path must not yield; the generator returns its missing list
    via StopIteration.value (plain functions are supported too)."""
    result = comboCls.y_combo(bot, True)
    if not hasattr(result, "send"):  # plain function, returned the list directly
        return result if result is not None else []
    try:
        next(result)
    except StopIteration as e:
        return e.value if e.value is not None else []
    ERROR_MSG("combo yielded during justCheck, treating as not runnable:", comboCls.__name__)
    return [None]


def evaluateCombos(bot):
    """Walk the bot config's combo list in priority order.

    Returns (readyName, almostPlan):
      readyName  = first combo whose justCheck returned []
      almostPlan = first supply-fixable combo (missing real cardKeys only)"""
    config = bot.getBotConfig()
    names = config.get("combos") or []
    ready = None
    almost = None
    for name in names:
        comboCls = COMBOS.get(name)
        if comboCls is None:
            ERROR_MSG("combo not registered:", name)
            continue
        missing = runJustCheck(comboCls, bot)
        if missing == []:
            ready = name
            break
        if almost is None and missing and None not in missing:
            almost = ComboPlan(name, missing)
    return ready, almost


# ============================================================
# Combos
# ============================================================

class Combo_dragonRush(ComboBase):
    """Two baby dragons as bodies, then tribute-summon the signature dragon."""

    # --- config ---
    NEED_KEYS = ["SK_BabyDragon", "SK_BabyDragon", "MountainDragon"]
    NEED_MONSTER_SPACE = 2
    STEP_WAIT = 1.5

    @staticmethod
    def y_combo(bot, justCheck):
        cfg = Combo_dragonRush
        game = bot.game
        side = bot.getSide()

        # ---- condition check (shared by both modes) ----
        missing = bot.missingInHand(cfg.NEED_KEYS)
        if game.freeMonsterSpace(side) < cfg.NEED_MONSTER_SPACE or not bot.canNormalSummonNow():
            # Not runnable this turn regardless of hand: None marks it unfixable
            missing = missing + [None]
        if justCheck:
            return missing

        # ---- execute (real hand cards, normal summon flow) ----
        ok = yield game.y_normalSummon(False, bot.handCard("SK_BabyDragon"))
        if not ok:
            return False
        yield WaitForSeconds(cfg.STEP_WAIT)
        yield game.y_normalSummon(False, bot.handCard("SK_BabyDragon"),
                                  costNormalSummonChance=False)
        yield WaitForSeconds(cfg.STEP_WAIT)
        # Tribute summon; the tribute selector is answered by aiChoice
        # (self_cost policy picks the weakest own monsters, i.e. the babies).
        ok = yield game.y_normalSummon(False, bot.handCard("MountainDragon"),
                                       costNormalSummonChance=False)
        if ok:
            bot.signatureOnField = True
        return ok


# ============================================================
# Auto registry: every ComboBase subclass in this module registers itself.
# Runs at import (and again on hot reload), so defining a class is enough.
# ============================================================
def _collectCombos():
    combos = {}
    for obj in list(globals().values()):
        if isinstance(obj, type) and issubclass(obj, ComboBase) and obj is not ComboBase:
            name = obj.getName()
            if name in combos:
                ERROR_MSG("duplicate combo name:", name, obj.__name__)
                continue
            combos[name] = obj
    return combos


COMBOS = _collectCombos()
