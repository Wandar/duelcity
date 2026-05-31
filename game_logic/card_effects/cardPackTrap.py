# -*- coding: utf-8 -*-
from __future__ import annotations
from annos import *
from KBEDebug import *
from a import Signal
from b.Card import *
from a.Effect import *
from a.DuelConstants import *
from Constants import *


"""
奈落 圣防 激流 活死人 神宣 神警

"""


"""
[对方从手牌或墓地召唤怪兽后]:将该怪兽变成防御表示
"""
class TrapSpecialSummonChangeForm(Effect):
    effType = EFF_TYPE.instant

    observeSignals = (LOCATION.spellTrapZone,[Signal.Summon])

    AI_HINT = [AI_HINT.debuff]
    EFF_POWER = 1
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal:Signal.Summon):
        if signal.card.preLocation==LOCATION.hand or signal.card.preLocation==LOCATION.grave:
            pass
        else:
            return False

        enemyTuple=self.getEnemySideTuple()
        if signal.card.side in enemyTuple:
            enemyCard=signal.card
        else:
            return False

        if justCheck:
            return True

        yield self.y_changeForm(enemyCard, FORM.defence)
        return True


"""
[]
"""


class battle_trap(Card):
    CARD_KEY="battle_trap"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(battle_trap_effect1)

class battle_trap_effect1(Effect):
    effType = EFF_TYPE.optionalInstant

    enablePlace = LOCATION.mask_onField
    observeSignals = [Signal.InBattle]

    _savedTarget1:Card=None

    def y_cost(self, justCheck:bool, signal:Signal.InBattle):
        if not isSignal(signal, Signal.InBattle):
            return False

        if signal.attackerCard.side==self.getSide():
            return False

        if justCheck:
            return True

        self.target=signal.card
        return True

    def y_activate(self, justCheck:bool, signal:Signal.InBattle):
        if justCheck:
            return True

        if self.target and self.target.isMonsterOnField():
            yield self.game.y_destroyCard(self.target)
            self.target=None


class CounterTrap(Card):
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(CounterTrap_effect1)

class CounterTrap_effect1(Effect):
    effType = EFF_TYPE.optionalInstant

    observeSignals = (LOCATION.spellTrapZone,[Signal.BeforeActivateEffect])

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 1
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal:Signal.BeforeActivateEffect):
        effect=signal.effect
        if effect.hasFlagCount(EFF_FLAG.activateCountered):
            return False

        if justCheck:
            return True

        effect.addFlagCount(EFF_FLAG.activateCountered)
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True
        return True



"""
OT:当你被怪兽直接攻击后,破坏该怪兽
"""
class DirectAttackDestroy(Effect):
    effType = EFF_TYPE.optionalTrigger

    observeSignals = (LOCATION.spellTrapZone,[Signal.BattleFinish])

    AI_HINT = [AI_HINT.eraser]
    AI_POWER = 1
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal:Signal.BattleFinish):
        if isSignal(signal,Signal.BattleFinish) and signal.battleType==BATTLE_TYPE.directAttack and signal.receiverPlayer==self.getSide():
            pass
        else:
            return

        attackMonster=signal.attackerCard
        if not attackMonster.isMonsterOnField():
            return
        if justCheck:
            return True

        self.saveTarget1(attackMonster)
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True

        target=self.getLegalTarget1()
        yield self.y_destroyCard(target)
        return True