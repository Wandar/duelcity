# -*- coding: utf-8 -*-
from __future__ import annotations

from card_effects.effectSummon import SpecialSummonWhileBattleDamage
from dutil import *
from annos import *
"""
CardName:Festering Ghoul
卡名:疮痂食尸鬼
"""

class ghoul_festering(Card):
    CARD_KEY="ghoul_festering"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(SpecialSummonWhileBattleDamage)
        pass
