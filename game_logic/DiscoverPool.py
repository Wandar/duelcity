# -*- coding: utf-8 -*-
"""
DiscoverPool — 全服全局发现卡池管理器（单例）

职责：
  - 按过滤条件（种族/属性/类型/等级范围）懒初始化卡池
  - 用洗牌队列保证同批次内不重复
  - 返回 cardKey 字符串列表，由调用方 createCard

用法（在 Effect 子类里）：
    keys = DiscoverPool.instance().get(race=RACE.DINOSAUR, count=3)
    tempCards = [self.game.createCard(k, self.getSide()) for k in keys]
    # 玩家选牌后加手牌，未选的 destroyTempCard

过滤参数均可省略（省略 = 不过滤该维度）：
    get(race=RACE.DINOSAUR)               # 所有恐龙族
    get(attr=ATTR.DARK, maxLevel=4)       # LV4以下暗属性
    get(cardType='SPELL')                 # 所有魔法卡
    get(minLevel=5)                       # LV5以上怪兽（默认只取怪兽）
    get(includeAllTypes=True, race=None)  # 怪兽+魔法+陷阱全部
"""
from __future__ import annotations

import random
from typing import Dict, List, Optional, Tuple

from KBEDebug import *
from globalvars import D_CARD
from Constants import RACE, ATTR

# ─────────────────────────────────────────────
# 枚举值 → D_CARD 字符串名称 的反查表
# D_CARD 里 race/attr 均以大写字符串存储，如 "DINOSAUR"、"DARK"
# ─────────────────────────────────────────────
_RACE_INT_TO_STR: Dict[int, str] = {
    1:  'WARRIOR',    2:  'SPELLCASTER', 4:  'FIEND',
    5:  'UNDEAD',     6:  'MACHINE',     7:  'AQUA',
    8:  'PYRO',       9:  'ROCK',        10: 'WINDBEAST',
    11: 'PLANT',      12: 'INSECT',      14: 'DRAGON',
    15: 'BEAST',      16: 'BEASTWARRIOR',17: 'DINOSAUR',
    20: 'REPTILE',    21: 'FAIRY',
}

_ATTR_INT_TO_STR: Dict[int, str] = {
    0x01: 'DARK',   0x02: 'LIGHT',  0x04: 'EARTH',
    0x08: 'WATER',  0x10: 'FIRE',   0x20: 'WIND',   0x40: 'GRASS',
}

# D_CARD type 字段包含的关键词 → 归属
_MONSTER_TYPE_KEYWORDS = ('MONSTER',)   # 'MONSTER'/'ORANGE_MONSTER'/'WHITE_MONSTER' 均含 'MONSTER'
_SPELL_TYPE_KEYWORDS   = ('SPELL',)
_TRAP_TYPE_KEYWORDS    = ('TRAP',)


def _toStr(val, table: Dict[int, str]) -> Optional[str]:
    """将枚举整数或字符串统一成 D_CARD 里的大写字符串；None 原样返回。"""
    if val is None:
        return None
    if isinstance(val, str):
        return val.upper()
    if isinstance(val, int):
        return table.get(val)
    return None


def _typeMatches(dtype: str, cardType) -> bool:
    """
    检查 D_CARD['type'] 字符串是否符合 cardType 过滤。
    cardType 可以是：
      None          → 只取怪兽（默认行为，此函数不会被调用，外层处理）
      'MONSTER'     → 含 'MONSTER' 的类型
      'SPELL'       → 含 'SPELL' 的类型
      'TRAP'        → 含 'TRAP' 的类型
      'ALL'/'all'   → 任意类型
    """
    if cardType is None:
        return 'MONSTER' in dtype
    ct = cardType.upper() if isinstance(cardType, str) else str(cardType).upper()
    if ct in ('ALL', 'ANY'):
        return True
    return ct in dtype


# ─────────────────────────────────────────────
# 内部池子：洗牌队列
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
        从洗牌队列里取 count 张不重复的 key。
        池子大小不足 count 时取全部。
        """
        if not self._all:
            return []
        count = min(count, len(self._all))
        result = []
        while len(result) < count:
            if not self._queue:
                self._refill()
            # 避免同次 pick 内重复（队列末尾可能恰好和已取的重叠）
            key = self._queue.pop()
            if key not in result:
                result.append(key)
        return result


# ─────────────────────────────────────────────
# 单例主体
# ─────────────────────────────────────────────
class DiscoverPool:
    _inst: Optional[DiscoverPool] = None

    def __init__(self):
        # key → _Pool
        self._pools: Dict[Tuple, _Pool] = {}

    # ── 单例 ──────────────────────────────────

    @classmethod
    def instance(cls) -> DiscoverPool:
        if cls._inst is None:
            cls._inst = DiscoverPool()
        return cls._inst

    @classmethod
    def reset(cls):
        """重载 ALL_DATA 后调用，清空所有缓存池（下次 get 时重新构建）。"""
        if cls._inst is not None:
            cls._inst._pools.clear()
        cls._inst = None
        INFO_MSG("[DiscoverPool] 已重置")

    # ── 主接口 ────────────────────────────────

    def get(self,
            race=None,
            attr=None,
            cardType=None,
            minLevel: int = None,
            maxLevel: int = None,
            onlyEnabled: bool = True,
            count: int = 3) -> List[str]:
        """
        返回 count 个满足条件的 cardKey 字符串。

        参数
        ----
        race        : RACE.DINOSAUR 或 'DINOSAUR'，None = 不过滤
        attr        : ATTR.DARK 或 'DARK'，None = 不过滤
        cardType    : 'MONSTER'/'SPELL'/'TRAP'/'ALL'，None = 只取怪兽
        minLevel    : 最小等级（含），None = 不限
        maxLevel    : 最大等级（含），None = 不限
        onlyEnabled : True = 只取 disable==9 的卡（已启用），False = 取所有
        count       : 返回张数，默认 3
        """
        raceStr = _toStr(race, _RACE_INT_TO_STR)
        attrStr = _toStr(attr, _ATTR_INT_TO_STR)

        fkey = (raceStr, attrStr, cardType, minLevel, maxLevel, onlyEnabled)

        if fkey not in self._pools:
            pool = self._buildPool(raceStr, attrStr, cardType, minLevel, maxLevel, onlyEnabled)
            self._pools[fkey] = pool
            INFO_MSG(f"[DiscoverPool] 新池子 race={raceStr} attr={attrStr} "
                     f"type={cardType} lv={minLevel}~{maxLevel} "
                     f"共 {len(pool)} 张")

        keys = self._pools[fkey].pick(count)

        if not keys:
            WARNING_MSG(f"[DiscoverPool] 池子为空 fkey={fkey}")
        return keys

    # ── 构建池子 ──────────────────────────────

    def _buildPool(self, raceStr, attrStr, cardType, minLevel, maxLevel, onlyEnabled) -> _Pool:
        keys = []
        for key, d in D_CARD.items():
            # 跳过版本号等非卡条目
            if not key or key == 'version':
                continue

            # 启用状态过滤
            if onlyEnabled and d.get('disable', 0) != 9:
                continue

            # 类型过滤
            dtype = d.get('type', '')
            if not _typeMatches(dtype, cardType):
                continue

            # 种族过滤
            if raceStr is not None and d.get('race', '') != raceStr:
                continue

            # 属性过滤
            if attrStr is not None and d.get('attr', '') != attrStr:
                continue

            # 等级过滤
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
