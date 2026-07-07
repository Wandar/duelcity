# -*- coding: utf-8 -*-
"""
DiscoverPool — Global singleton for Hearthstone-style Discover card pool management.

Responsibilities:
  - Lazy-initialize pools by filter conditions (race / attr / type / level range)
  - Support manually registered named pools (explicit card key lists)
  - Shuffle-bag to avoid repetition within the same batch
  - Return cardKey string lists; callers are responsible for createCard

── Auto filter pool (built from ALL_DATA) ──────────────────────
    keys = DiscoverPool.instance().get(race=RACE.DINOSAUR, count=3)

All filter params are optional (omit = no filter on that dimension) and take
Constants enums, never strings:
    get(race=RACE.DINOSAUR)               # all dinosaur-race cards
    get(attr=ATTR.DARK, maxLevel=4)       # dark-attr cards LV4 or below
    get(cardType=CARD_TYPE.spell)         # all spell cards
    get(minLevel=5)                       # monsters LV5 or above (default: monsters only)

── Manual named pool (explicit card key list) ────────────────────────
Register (typically at game init or stage config):
    DiscoverPool.instance().registerPool('boss_drops', [
        'FireDragonRed', 'Dragonknight', 'ElderDragon_Rd',
    ])

Discover:
    keys = DiscoverPool.instance().getFromPool('boss_drops', count=3)
    tempCards = [self.game.createCard(k, self.getSide()) for k in keys]
    # add picked card to hand; destroy the rest (temp cards)

Remove:
    DiscoverPool.instance().unregisterPool('boss_drops')
"""
from __future__ import annotations

from util import *

from KBEDebug import *
from globalvars import D_CARD
from Constants import RACE, ATTR, CARD_TYPE

def _enumToStr(val, enumCls) -> Optional[str]:
    """
    Reverse-lookup a Constants MyEnum int value to its member name string.
    D_CARD stores race/attr as uppercase strings identical to the enum member
    names (e.g. RACE.DINOSAUR=17 -> 'DINOSAUR'), so the name IS the D_CARD string.
    Pass None through; 'none' and private members are skipped.
    """
    if val is None:
        return None
    if not isinstance(val, int):
        ERROR_MSG(f"[DiscoverPool] expected a Constants enum int, got {val!r}")
        return None
    for name, v in vars(enumCls).items():
        if name.startswith('_') or name == 'none':
            continue
        if v == val:
            return name
    ERROR_MSG(f"[DiscoverPool] no {enumCls.__name__} member with value {val!r}")
    return None


def _typeMatches(dtype: str, cardType) -> bool:
    """
    Check whether a D_CARD['type'] string matches the cardType filter.
    cardType is a Constants CARD_TYPE enum:
      None              -> monsters only (default)
      CARD_TYPE.all     -> any type
      CARD_TYPE.monster -> types containing 'MONSTER' (incl. fusion/orange/white)
      CARD_TYPE.spell   -> types containing 'SPELL'  (incl. continuous/equip)
      CARD_TYPE.trap    -> types containing 'TRAP'   (incl. continuous)
    Bitmask tests are used so monster/spell/trap subtype enums also match.
    """
    if cardType is None:
        return 'MONSTER' in dtype
    if not isinstance(cardType, int):
        ERROR_MSG(f"[DiscoverPool] cardType expects a CARD_TYPE enum, got {cardType!r}")
        return False
    if cardType == CARD_TYPE.all:
        return True
    if cardType & CARD_TYPE.monster:
        return 'MONSTER' in dtype
    if cardType & CARD_TYPE.spell:
        return 'SPELL' in dtype
    if cardType & CARD_TYPE.trap:
        return 'TRAP' in dtype
    return False


# ─────────────────────────────────────────────
# Internal pool: shuffle-bag queue
# ─────────────────────────────────────────────
class _Pool:
    __slots__ = ('_all', '_queue')

    def __init__(self, keys: List[str]):
        self._all: List[str] = list(keys)
        self._queue: List[str] = []

    def __len__(self):
        return len(self._all)

    def _refill(self):
        self._queue = list(self._all)
        random.shuffle(self._queue)

    def pick(self, count: int) -> List[str]:
        """
        Draw count unique keys from the shuffle-bag.
        If the pool has fewer than count cards, return all of them.
        """
        if not self._all:
            return []
        count = min(count, len(self._all))
        result = []
        while len(result) < count:
            if not self._queue:
                self._refill()
            # Guard against duplicates when the tail of one cycle overlaps the next
            key = self._queue.pop()
            if key not in result:
                result.append(key)
        return result


# ─────────────────────────────────────────────
# Singleton
# ─────────────────────────────────────────────
class DiscoverPool(Reload):
    _inst: Optional[DiscoverPool] = None

    def __init__(self):
        Reload.__init__(self, True, True)
        # filter-key tuple → _Pool  (auto-built pools)
        self._pools: Dict[Tuple, _Pool] = {}
        # name → _Pool  (manually registered pools)
        self._named_pools: Dict[str, _Pool] = {}
        self._reset()

    # ── Singleton ─────────────────────────────

    def _reset(self):
        """Clear auto-built pools (called after ALL_DATA reload).
        Named pools are intentionally preserved — their keys come from external config."""
        if self._inst is not None:
            self._inst._pools.clear()
        self._inst = None

    @classmethod
    def instance(cls) -> DiscoverPool:
        if cls._inst is None:
            cls._inst = DiscoverPool()
        return cls._inst

    def onReloadData(self):
        self._reset()

    # ── Manual named pools ────────────────────

    def registerPool(self, name: str, keys: List[str]):
        """
        Register a named pool with an explicit card key list.

        Parameters
        ----------
        name : pool identifier used when calling getFromPool
        keys : list of cardKey strings; duplicates are allowed (acts as weight)

        Example
        -------
        DiscoverPool.instance().registerPool('boss_drops', [
            'FireDragonRed', 'Dragonknight', 'ElderDragon_Rd',
        ])
        """
        self._named_pools[name] = _Pool(list(keys))
        INFO_MSG(f"[DiscoverPool] registered named pool '{name}' with {len(keys)} cards")

    def unregisterPool(self, name: str):
        """Remove a named pool by name."""
        if name in self._named_pools:
            del self._named_pools[name]
            INFO_MSG(f"[DiscoverPool] removed named pool '{name}'")

    def getFromPool(self, name: str, count: int = 3) -> List[str]:
        """
        Draw count cards from a named pool; returns a list of cardKey strings.
        Returns an empty list (with a WARNING) if the pool does not exist.

        Example
        -------
        keys = DiscoverPool.instance().getFromPool('boss_drops', count=3)
        tempCards = [self.game.createCard(k, self.getSide()) for k in keys]
        """
        pool = self._named_pools.get(name)
        if pool is None:
            WARNING_MSG(f"[DiscoverPool] named pool '{name}' not found — call registerPool first")
            return []
        keys = pool.pick(count)
        if not keys:
            WARNING_MSG(f"[DiscoverPool] named pool '{name}' is empty")
        return keys

    def hasPool(self, name: str) -> bool:
        """Return True if a named pool with the given name exists."""
        return name in self._named_pools

    # ── Auto filter pool ──────────────────────

    def get(self,
            race=None,
            attr=None,
            cardType=None,
            minLevel: int = None,
            maxLevel: int = None,
            onlyEnabled: bool = True,
            count: int = 3) -> List[str]:
        """
        Return count cardKey strings that match the given filters.

        Parameters
        ----------
        race        : RACE enum (e.g. RACE.DINOSAUR); None = no filter
        attr        : ATTR enum (e.g. ATTR.DARK); None = no filter
        cardType    : CARD_TYPE enum (monster/spell/trap/all); None = monsters only
        minLevel    : minimum level (inclusive); None = no limit
        maxLevel    : maximum level (inclusive); None = no limit
        onlyEnabled : True = only cards with disable==9; False = all cards
        count       : number of cards to return (default 3)
        """
        raceStr = _enumToStr(race, RACE)
        attrStr = _enumToStr(attr, ATTR)

        fkey = (raceStr, attrStr, cardType, minLevel, maxLevel, onlyEnabled)

        if fkey not in self._pools:
            pool = self._buildPool(raceStr, attrStr, cardType, minLevel, maxLevel, onlyEnabled)
            self._pools[fkey] = pool
            INFO_MSG(f"[DiscoverPool] new auto pool race={raceStr} attr={attrStr} "
                     f"type={cardType} lv={minLevel}~{maxLevel} "
                     f"size={len(pool)}")

        keys = self._pools[fkey].pick(count)

        # Fallback: not enough matching cards — rediscover without the level
        # limits (race/attr/type filters are kept) and top up the result.
        if len(keys) < count and (minLevel is not None or maxLevel is not None):
            INFO_MSG(f"[DiscoverPool] only {len(keys)}/{count} cards for fkey={fkey}, "
                     f"retrying without level limits")
            fkey2 = (raceStr, attrStr, cardType, None, None, onlyEnabled)
            if fkey2 not in self._pools:
                pool2 = self._buildPool(raceStr, attrStr, cardType, None, None, onlyEnabled)
                self._pools[fkey2] = pool2
                INFO_MSG(f"[DiscoverPool] new auto pool race={raceStr} attr={attrStr} "
                         f"type={cardType} lv=None~None size={len(pool2)}")
            extra = self._pools[fkey2].pick(count)
            for k in extra:
                if len(keys) >= count:
                    break
                if k not in keys:
                    keys.append(k)

        if not keys:
            WARNING_MSG(f"[DiscoverPool] auto pool is empty fkey={fkey}")
        return keys

    # ── Build auto pool ───────────────────────

    def _buildPool(self, raceStr, attrStr, cardType, minLevel, maxLevel, onlyEnabled) -> _Pool:
        keys = []
        for key, d in D_CARD.items():
            # skip meta entries like 'version'
            if not key or key == 'version':
                continue

            # enabled filter
            if onlyEnabled and d.get('disable', 0) != 9:
                continue

            # type filter
            dtype = d.get('type', '')
            if not _typeMatches(dtype, cardType):
                continue

            # race filter
            if raceStr is not None and d.get('race', '') != raceStr:
                continue

            # attr filter
            if attrStr is not None and d.get('attr', '') != attrStr:
                continue

            # level filter
            if minLevel is not None or maxLevel is not None:
                try:
                    lv = int(d.get('level', 0) or 0)
                except (ValueError, TypeError):
                    lv = 0
                if minLevel is not None and lv < minLevel:
                    continue
                if maxLevel is not None and lv > maxLevel:
                    continue

            keys.append(key)

        return _Pool(keys)
