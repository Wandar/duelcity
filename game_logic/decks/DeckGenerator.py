# -*- coding: utf-8 -*-
"""
DeckGenerator -- automatic deck builder.

Inputs:
  - tendency  deck tendency ('aggro' / 'midrange' / 'control'); sets the level curve
              and the number of spell/trap cards
  - races     preferred race list (e.g. ['DRAGON','MACHINE']); these races' monsters
              are filled first, falling back to all monsters when short
  - keyCards  forced-include card keys ('Wyvern' or ('Wyvern', 3) with a copy count)
  - rules     optional override of the build quota (low / high / spell / trap counts)

Build quota (defaults come from the tendency preset, overridable via `rules`):
  low   : number of LV<=4 monsters
  high  : number of LV>=5 monsters
  spell : number of spell cards
  trap  : number of trap cards
  the four values sum to deckSize (default 40)

Running this file directly -> prints one deck in JSON (the {"a":[...]} shape used in decks.py).

D_CARD init follows gamble.py: use globalvars.D_CARD inside the engine; standalone it is
loaded from data.fods via fodsReader.reloadDataRelease(), falling back to ALL_DATA.json.
"""
from __future__ import annotations
import json
import os
import sys
import random
from collections import Counter
from enum import Enum
from typing import List, Dict, Tuple, Union, Optional

# ─────────────────────────────────────────────
# D_CARD init (follows gamble.py)
# ─────────────────────────────────────────────
def _load_d_card():
    # 1. inside the engine: globalvars.D_CARD is already populated
    try:
        from globalvars import D_CARD as raw
        if raw:
            return raw
    except Exception:
        pass
    # 2. standalone: load from data.fods via fodsReader, same as gamble.py. fodsReader
    #    lives in <root>/sec/data and (outside the engine) reads "data.fods" by filename
    #    from the cwd, so put that folder on sys.path and run the reload with cwd switched
    #    there. reloadDataRelease() fills its D_CARD dict in place as {key: entry}.
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    secData = os.path.join(root, "sec", "data")
    try:
        if secData not in sys.path:
            sys.path.insert(0, secData)
        import fodsReader
        cwd = os.getcwd()
        try:
            os.chdir(secData)
            fodsReader.reloadDataRelease()
        finally:
            os.chdir(cwd)
        if fodsReader.D_CARD:
            return fodsReader.D_CARD
    except Exception as ex:
        print("[DeckGenerator] fodsReader load failed, fallback to ALL_DATA.json:", ex)
    # 3. last resort: read the generated ALL_DATA.json
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "..", "ALL_DATA.json"), encoding="utf-8") as f:
        return json.load(f)["D_CARD"]


_RAW = _load_d_card()

# normalize to {cardKey: entry}
if isinstance(_RAW, dict):
    D_CARD: Dict[str, dict] = _RAW
else:
    D_CARD = {e["key"]: e for e in _RAW
              if isinstance(e, dict) and e.get("key") and e.get("key") != "version"}


# ─────────────────────────────────────────────
# card-field accessors
# ─────────────────────────────────────────────
def _enabled(e: dict) -> bool:
    return e.get("disable") == 9

def _cardType(e: dict) -> str:
    t = e.get("type", "")
    if "MONSTER" in t:
        return "MONSTER"
    if "SPELL" in t:
        return "SPELL"
    if "TRAP" in t:
        return "TRAP"
    return "?"

def _level(e: dict) -> int:
    try:
        return int(e.get("level", 0) or 0)
    except (TypeError, ValueError):
        return 0

def _bt(e: dict) -> int:
    # power tier (2~5), used as the selection weight
    try:
        return int(e.get("extradata", {}).get("bt", 2) or 2)
    except (TypeError, ValueError):
        return 2


# ─────────────────────────────────────────────
# deck tendency
# ─────────────────────────────────────────────
class Tendency(Enum):
    AGGRO = "aggro"        # low-level pressure
    MIDRANGE = "midrange"  # balanced
    CONTROL = "control"    # high-level + control


# tendency presets (the four counts sum to deckSize=40)
TENDENCY_PRESETS: Dict[Tendency, Dict[str, int]] = {
    Tendency.AGGRO:    {"low": 28, "high": 4,  "spell": 6, "trap": 2},
    Tendency.MIDRANGE: {"low": 22, "high": 10, "spell": 6, "trap": 2},
    Tendency.CONTROL:  {"low": 14, "high": 14, "spell": 8, "trap": 4},
}


def _candidatePool(predicate) -> List[str]:
    return [k for k, e in D_CARD.items() if _enabled(e) and predicate(e)]


def _pickWithCopies(pool: List[str], need: int, taken: Counter,
                    maxCopies: int, copiesRange=(2, 3)) -> List[str]:
    """
    Pick distinct cards from `pool` weighted by power (bt), adding 2~3 copies each until
    `need` cards are gathered. `taken` tracks copies already in the deck so the global
    per-card cap (maxCopies) is never exceeded. Returns the list of keys added.
    """
    if need <= 0 or not pool:
        return []
    # higher bt first, plus random jitter to keep variety
    ordered = sorted(pool, key=lambda k: _bt(D_CARD[k]) + random.random() * 2, reverse=True)
    result: List[str] = []
    for k in ordered:
        if need <= 0:
            break
        room = maxCopies - taken[k]
        if room <= 0:
            continue
        c = min(random.randint(*copiesRange), room, need)
        if c <= 0:
            continue
        taken[k] += c
        result += [k] * c
        need -= c
    return result


def generate_deck(tendency: Union[Tendency, str] = Tendency.MIDRANGE,
                  races: Optional[List[str]] = None,
                  keyCards: Optional[List[Union[str, Tuple[str, int]]]] = None,
                  rules: Optional[Dict[str, int]] = None,
                  deckSize: int = 40,
                  maxCopies: int = 3,
                  seed: Optional[int] = None) -> Dict[str, List[str]]:
    """
    Build a deck from a tendency / preferred races / key cards / quota rules.

    Args:
        tendency: Deck tendency (Tendency enum) selecting the level-curve preset and
                  spell/trap counts: Tendency.AGGRO (low-level pressure),
                  Tendency.MIDRANGE (balanced) or Tendency.CONTROL (high-level + control).
                  A plain string value ('aggro'/'midrange'/'control') is also accepted;
                  unknown values fall back to MIDRANGE.
        races:    Preferred monster races (e.g. ['DRAGON','MACHINE']); matched case-
                  insensitively against D_CARD 'race'. These are filled first, then any
                  monster is used to cover the shortfall. None/empty = no race preference.
        keyCards: Cards forced into the deck. Each item is either a key string ('Wyvern',
                  defaults to 2 copies) or a (key, copies) tuple. Copies are capped at
                  maxCopies; each key card counts against its matching quota bucket.
                  Unknown keys are skipped with a warning.
        rules:    Optional overrides for the quota dict, merged over the tendency preset.
                  Keys: 'low' (LV<=4 monsters), 'high' (LV>=5 monsters), 'spell', 'trap'.
                  e.g. {'low': 30, 'high': 4, 'spell': 4, 'trap': 2}.
        deckSize: Target total number of cards (default 40). The deck is padded with extra
                  low-level monsters if short and truncated if over.
        maxCopies: Maximum copies of any single card key in the deck (default 3).
        seed:     Optional RNG seed for reproducible decks; None = nondeterministic.

    Returns:
        A deck dict in decks.py shape: {"a": [cardKey, ...]} with len == deckSize.

    Notes:
        Only enabled cards (disable == 9) are eligible. Card selection is weighted by the
        power tier (extradata.bt, 2~5) plus random jitter, so stronger cards are favored
        while keeping variety.
    """
    if seed is not None:
        random.seed(seed)
    races = [r.upper() for r in (races or [])]

    # normalize tendency (accept a Tendency or its string value)
    if not isinstance(tendency, Tendency):
        try:
            tendency = Tendency(str(tendency).lower())
        except ValueError:
            tendency = Tendency.MIDRANGE

    # 1. quota: preset + overrides
    plan = dict(TENDENCY_PRESETS[tendency])
    if rules:
        plan.update(rules)

    taken: Counter = Counter()
    deck: List[str] = []

    def add(keys: List[str]):
        deck.extend(keys)

    # 2. forced key cards (counted against their quota bucket)
    for item in (keyCards or []):
        k, copies = (item if isinstance(item, tuple) else (item, 2))
        if k not in D_CARD:
            print("[DeckGenerator] unknown key card, skipped:", k)
            continue
        copies = min(copies, maxCopies)
        taken[k] += copies
        add([k] * copies)
        e = D_CARD[k]
        t = _cardType(e)
        if t == "MONSTER":
            bucket = "low" if _level(e) <= 4 else "high"
        elif t == "SPELL":
            bucket = "spell"
        elif t == "TRAP":
            bucket = "trap"
        else:
            bucket = None
        if bucket:
            plan[bucket] = max(0, plan[bucket] - copies)

    # 3. monsters: preferred races first, then fall back to all monsters
    inRace = lambda e: (not races) or (e.get("race") in races)

    lowPref = _candidatePool(lambda e: _cardType(e) == "MONSTER" and _level(e) <= 4 and inRace(e))
    lowAny  = _candidatePool(lambda e: _cardType(e) == "MONSTER" and _level(e) <= 4)
    add(_pickWithCopies(lowPref, plan["low"], taken, maxCopies))
    # cover the low shortfall with any low-level monster
    add(_pickWithCopies([k for k in lowAny if k not in set(lowPref)],
                        max(0, plan["low"] - _countBucket(deck, "low")), taken, maxCopies))

    highPref = _candidatePool(lambda e: _cardType(e) == "MONSTER" and _level(e) >= 5 and inRace(e))
    highAny  = _candidatePool(lambda e: _cardType(e) == "MONSTER" and _level(e) >= 5)
    add(_pickWithCopies(highPref, plan["high"], taken, maxCopies))
    add(_pickWithCopies([k for k in highAny if k not in set(highPref)],
                        max(0, plan["high"] - _countBucket(deck, "high")), taken, maxCopies))

    # 4. spells / traps
    spellPool = _candidatePool(lambda e: _cardType(e) == "SPELL")
    trapPool  = _candidatePool(lambda e: _cardType(e) == "TRAP")
    add(_pickWithCopies(spellPool, max(0, plan["spell"] - _countBucket(deck, "spell")), taken, maxCopies))
    add(_pickWithCopies(trapPool,  max(0, plan["trap"]  - _countBucket(deck, "trap")),  taken, maxCopies))

    # 5. reach deckSize: pad with any low-level monster if short, truncate if over
    add(_pickWithCopies(lowAny, max(0, deckSize - len(deck)), taken, maxCopies, copiesRange=(1, 2)))
    deck = deck[:deckSize]

    return {"a": deck}


def _countBucket(deck: List[str], bucket: str) -> int:
    n = 0
    for k in deck:
        e = D_CARD.get(k)
        if not e:
            continue
        t = _cardType(e)
        if bucket == "low" and t == "MONSTER" and _level(e) <= 4:
            n += 1
        elif bucket == "high" and t == "MONSTER" and _level(e) >= 5:
            n += 1
        elif bucket == "spell" and t == "SPELL":
            n += 1
        elif bucket == "trap" and t == "TRAP":
            n += 1
    return n


def deck_summary(deck: Dict[str, List[str]]) -> str:
    keys = deck["a"]
    low = _countBucket(keys, "low")
    high = _countBucket(keys, "high")
    sp = _countBucket(keys, "spell")
    tr = _countBucket(keys, "trap")
    races = Counter(D_CARD[k].get("race") for k in keys if k in D_CARD and _cardType(D_CARD[k]) == "MONSTER")
    return (f"total {len(keys)} | lowMon {low} highMon {high} spell {sp} trap {tr} "
            f"| races {dict(races.most_common(5))}")


# ─────────────────────────────────────────────
# run directly -> output a JSON deck
# ─────────────────────────────────────────────
if __name__ == "__main__":
    deck = generate_deck(
        tendency=Tendency.MIDRANGE,
        races=["DRAGON"],
        keyCards=[("Wyvern", 2), ("dragonrex", 1)],
        seed=1,
    )
    import sys
    print("// " + deck_summary(deck), file=sys.stderr)
    print(json.dumps(deck, ensure_ascii=False, indent=4))
