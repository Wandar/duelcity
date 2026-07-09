# -*- coding: utf-8 -*-
from __future__ import annotations

from util import *
from annos import *
from a.DuelConstants import *
from KBEngine import *

"""
botConfig: BotConfig (one bot's AI config) + deck generation.

Kept in its own module so botPack1.py stays MENU_BOTS-only. Built by
tryStartDuelWithBot and handed to the bot's AI (self.botConfig); the same
instance drives deck generation (buildBotDeck) and is read by the AI at
runtime (DuelAINormal.getBotConfig). One source of truth.

MENU_BOTS lives in botPack1; it is imported lazily inside fromMenuBot to
avoid an import cycle (botPack1 -> aiBrain -> botConfig -> botPack1).
"""

ALL_BOT_RACES = [RACE.DRAGON, RACE.AQUA, RACE.INSECT, RACE.PLANT,
                 RACE.BEASTWARRIOR, RACE.BEAST, RACE.FAIRY, RACE.DINOSAUR]


class BotConfig:
    def __init__(self, preferRace=None, preferCards=None, signatureMonsters=None,
                 combos=None, destroyCards=None, botWinRate=0.5, funTurns=3,
                 signatureTurn=6, avatarKey="", deck=None):
        self.preferRace        = preferRace
        self.preferCards       = list(preferCards or [])
        self.signatureMonsters = list(signatureMonsters or [])
        self.combos            = list(combos or [])
        self.destroyCards      = list(destroyCards or [])
        self.botWinRate        = botWinRate
        self.funTurns          = funTurns
        self.signatureTurn     = signatureTurn
        self.avatarKey         = avatarKey
        self.deck              = deck

    # Back-compat: AI code still reads config.get("preferCards") etc.
    def get(self, key, default=None):
        return getattr(self, key, default)

    @classmethod
    def fromMenuBot(cls, botName):
        """A MENU_BOTS bot: build the config from its entry."""
        from duelbot.botPack1 import MENU_BOTS      # lazy: avoid import cycle
        d = MENU_BOTS.get(botName, {}) or {}
        return cls(
            preferRace        = d.get("preferRace"),
            preferCards       = d.get("preferCards"),
            signatureMonsters = d.get("signatureMonsters"),
            combos            = d.get("combos"),
            destroyCards      = d.get("destroyCards"),
            botWinRate        = d.get("botWinRate", 0.5),
            funTurns          = d.get("funTurns", 3),
            signatureTurn     = d.get("signatureTurn", 6),
            avatarKey         = d.get("avatarKey", ""),
            deck              = d.get("deck"),
        )

    @classmethod
    def random(cls):
        """A non-MENU_BOTS in-scene bot: roll a random config."""
        race = random.choice(ALL_BOT_RACES)
        return cls(
            preferRace        = race,
            preferCards       = [],                              # filled by race in buildBotDeck / pools
            signatureMonsters = _pickMonstersByRace(race, 7, 999, count=3),
            combos            = [],
            botWinRate        = round(random.uniform(0.2, 0.5), 2),
            funTurns          = random.randint(2, 4),
            signatureTurn     = random.randint(5, 8),
        )


# ------------------------------------------------------------
# Deck generation from a BotConfig -> deck json {'a':[...], 'b':[...]}
# ------------------------------------------------------------
def _isMonsterKey(cardKey):
    j = D_CARD.get(cardKey)
    if not j:
        return False
    try:
        return bool(cardTypeStrToInt(j["type"], cardKey) & CARD_TYPE.monster)
    except Exception:
        return False


def _isWhiteMonsterKey(cardKey):
    j = D_CARD.get(cardKey)
    if not j:
        return False
    try:
        t = cardTypeStrToInt(j["type"], cardKey)
    except Exception:
        return False
    return (t & CARD_TYPE.whiteMonster) == CARD_TYPE.whiteMonster


def _matchRace(cardKey, preferRace):
    if not preferRace:
        return True
    j = D_CARD.get(cardKey)
    if not j:
        return False
    try:
        r = cardRaceStrToInt(j["race"], cardKey)
    except Exception:
        return False
    if isinstance(preferRace, (list, tuple, set)):
        return r in preferRace
    return r == preferRace


def _pickMonstersByRace(preferRace, lvMin, lvMax, count):
    """Random `count` non-fusion monster cardKeys of the given race/level range."""
    out = []
    for cardKey, j in D_CARD.items():
        if cardKey == "version":
            continue
        if not _isMonsterKey(cardKey) or _isWhiteMonsterKey(cardKey):
            continue
        lv = j.get("level", 0)
        if lv < lvMin or lv > lvMax:
            continue
        if not _matchRace(cardKey, preferRace):
            continue
        out.append(cardKey)
    random.shuffle(out)
    return out[:count]


def _supplementDeckList(deckList, targetSize, lvMin, lvMax, preferRace):
    """Pad deckList up to targetSize with low-level monsters of preferRace
    (relax the race filter if that race has too few)."""
    need = targetSize - len(deckList)
    if need <= 0:
        return

    def _collect(useRace):
        res = []
        for cardKey, j in D_CARD.items():
            if cardKey == "version":
                continue
            if not _isMonsterKey(cardKey) or _isWhiteMonsterKey(cardKey):
                continue
            lv = j.get("level", 0)
            if lv < lvMin or lv > lvMax:
                continue
            if useRace and not _matchRace(cardKey, preferRace):
                continue
            res.append(cardKey)
        return res

    pool = _collect(True)
    if len(pool) * 3 < need:
        pool = _collect(False) or pool
    if not pool:
        return
    random.shuffle(pool)
    i = 0
    while need > 0:
        deckList.append(pool[i % len(pool)])
        i += 1
        need -= 1


def buildBotDeck(botConfig, mainSize=40):
    """Generate a deck json from a BotConfig. a=main deck, b=extra (fusion/synchro)."""
    if botConfig is None:
        botConfig = BotConfig()
    a = []
    for k in botConfig.signatureMonsters:
        if k in D_CARD and not _isWhiteMonsterKey(k):
            a += [k] * 2                      # signature big monsters: 2 copies each
    for k in botConfig.preferCards:
        if k in D_CARD:
            a += [k] * 3                      # core cards: 3 copies each
    _supplementDeckList(a, mainSize, 1, 4, botConfig.preferRace)   # pad with small monsters
    b = [k for k in botConfig.signatureMonsters
         if k in D_CARD and _isWhiteMonsterKey(k)]                 # fusion/synchro -> extra deck
    return {"a": a[:mainSize], "b": b}
