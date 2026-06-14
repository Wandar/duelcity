# -*- coding: utf-8 -*-
from __future__ import annotations
from annos import *
from a.DuelConstants import *
from Constants import *
from typing import *

AUTO_GEN="AUTO_GEN"

class Signal:
    IS_LEAVE_SOMEWHERE=False
    card = None
    reasonCard:Card = None
    reasonEffect:Effect=None
    reasonEffectPeriod:EFF_PERIOD=0

    def __init__(self, card=None, reasonCard=None,reasonEffect=None,reasonEffectPeriod:EFF_PERIOD=0):
        self.card = card
        self.reasonCard = reasonCard
        self.reasonEffect=reasonEffect
        self.reasonEffectPeriod=reasonEffectPeriod

    def getName(self):
        return self.__class__.__name__

    def getSelfAndFatherSignalNames(self):
        # read from this class's own __dict__ only; getattr would walk the MRO and
        # let a subclass inherit its parent's cached list, dropping its own name
        allNames=self.__class__.__dict__.get("__ALL_SIGNAL__", None)
        if allNames==None:
            base_classes = list(self.__class__.__bases__)
            all_base_classes = set(base_classes)
            all_base_classes.add(self.__class__)

            while base_classes:
                current_class = base_classes.pop()
                parent_classes = current_class.__bases__
                all_base_classes.update(parent_classes)
                base_classes.extend(parent_classes)

            allNames=[n.__name__ for n in all_base_classes if n.__name__!="object"]
            allNames.remove("Signal")

            setattr(self.__class__,"__ALL_SIGNAL__",allNames)

        return allNames



"""
Player actively use effect
"""
class PlayerActivate(Signal):
    pass



##########################Game

class DrawCard(Signal):
    cardList=None

class DrawPhase(DrawCard):
    cardList:List[Card]=None #drew cards

class StandbyPhase(Signal):
    pass

class ChangePhaseToBattle(Signal):
    pass

class ChangePhaseToMainPhase2(Signal):
    pass

class TurnEnds(Signal):
    pass

class DrawCardsByEffect(DrawCard):
    cardList:List[Card]=None
    sideTuple:Tuple[int]=None


###########################Card Changes Place
class EnterField(Signal):
    preLocation=LOCATION.monsterZone
    card=None

class EnterHand(Signal):
    preLocation=LOCATION.monsterZone
    card=None

class EnterDeck(Signal):
    preLocation=LOCATION.monsterZone
    card=None

class EnterExtraDeck(Signal):
    preLocation=LOCATION.monsterZone
    card=None

class EnterGrave(Signal):
    preLocation=LOCATION.monsterZone
    card=None

class EnterBanished(Signal):
    preLocation=LOCATION.monsterZone
    card=None

#called before Destroy/Banish
#switching controller will not trigger this
class LeaveField(Signal):
    IS_LEAVE_SOMEWHERE=True
    card=None
    preHP=0

class LeaveHand(Signal):
    IS_LEAVE_SOMEWHERE=True
    card=None

class LeaveDeck(Signal):
    IS_LEAVE_SOMEWHERE=True
    card=None

class LeaveExtraDeck(Signal):
    IS_LEAVE_SOMEWHERE=True
    card=None

class LeaveGrave(Signal):
    IS_LEAVE_SOMEWHERE=True
    card=None

class LeaveBanished(Signal):
    IS_LEAVE_SOMEWHERE=True
    card=None


#called before Summon
#switching controller also triggers this.
class AttachMonsterZone(Signal):
    side=0
    preLocation=LOCATION.monsterZone
    card=None

# switching controller also triggers this.
class DetachMonsterZone(Signal):
    IS_LEAVE_SOMEWHERE=True
    preHP=0
    side=0
    card=None

class AttachSpellZone(Signal):
    side=0
    preLocation=LOCATION.monsterZone
    card=None

class DetachSpellZone(Signal):
    IS_LEAVE_SOMEWHERE=True
    side=0
    card=None

########################Summon

class Summon(Signal):
    pass

class NormalSummon(Summon):
    tributes:List[Card] = None

class SpecialSummon(Summon):
    pass

class SpecialSummonMultiCards(Summon):
    cardList:List[Card]=None

class ExtraSummon(SpecialSummon):
    tributes:List[Card] = None


#################################


#################################Card Be Do Something
class BeforeRemovedByEffect(Signal):
    cardList=None # cards will leave field
    removeType="destroy" #destroy tribute banish returnCardToDeck returnCardToHand sendCardToGrave  setCardToSpellZone  moveCardToSpellZone control

    def getDamageFx(self):
        removeType=self.removeType
        if removeType=="destroy":
            return FX_ID.effectDestroy
        elif removeType=="tribute":
            return FX_ID.sacrificeCircle
        elif removeType=="banish":
            return FX_ID.banish
        elif removeType=="returnCardToDeck":
            return FX_ID.returnToDeck
        elif removeType=="returnCardToHand":
            return FX_ID.returnToHand
        elif removeType=="sendCardToGrave":
            return FX_ID.effectDamage
        elif removeType=="setCardToSpellZone":
            return FX_ID.effectDamage
        elif removeType=="moveCardToSpellZone":
            return FX_ID.effectDamage
        elif removeType=="control":
            return FX_ID.effectDamage
        return FX_ID.effectDamage


class Tributed(Signal):pass
#Dont add TributedByNormalSummon And TributedBySynchroSummon

class Destroyed(Signal):
    IS_LEAVE_SOMEWHERE=True
class DestroyedOnField(Destroyed):pass
class DestroyedByBattle(DestroyedOnField):
    card=None
    reasonCard = None

class DestroyedOnFieldByEffect(DestroyedOnField):pass
class DestroyedByEffect(Destroyed):pass


class MonsterChangeController(Signal):
    card=None
#############################Battle

#before monster rushing,monster wants to battle but has not rushed
class RequestBattle(Signal):
    attackerCard=None
    receiverCard=None
    receiverPlayer:int=0
    battleType:BATTLE_TYPE=0


#monster rushed and is swinging its weapon,battle damage is not calculated
class InBattle(Signal):
    battleUniID=0
    attackerCard:Card=None
    receiverCard:Card=None
    receiverPlayer:int=0
    battleType:BATTLE_TYPE=0
    involvedSideList:List[int]=None
    activatedEffectList:List[Effect]=None
    def getMyCard(self,mySide):
        if self.attackerCard.side==mySide:
            return self.attackerCard
        elif self.battleType==BATTLE_TYPE.directAttack and self.receiverPlayer==mySide:
            return self.receiverPlayer
        elif self.receiverCard.side==mySide:
            return self.receiverCard
        return None

    def getBattleEnemy(self,mySide):
        if self.attackerCard.side==mySide:
            if self.battleType==BATTLE_TYPE.directAttack:
                return self.receiverPlayer
            else:
                return self.receiverCard
        else:
            return self.attackerCard


#battle finished,after card leave field
class BattleFinish(Signal):
    attackerCard:Card=None
    receiverCard:Card=None
    receiverPlayer:int=0
    battleType:BATTLE_TYPE = 0


class RangedAttackFinish(Signal):
    pass


##########################CardData
class CardDataChanged(Signal):
    pass

class CardAtkChanged(CardDataChanged):
    card:Card=None

class CardDefenceChanged(CardDataChanged):
    card:Card=None

class CardLevelChanged(CardDataChanged):
    card:Card=None

class CardAttrChanged(CardDataChanged):
    card:Card=None

class CardRaceChanged(CardDataChanged):
    card:Card=None


class CardEffectChanged(CardDataChanged):
    pass



class CardChangeForm(CardDataChanged):
    card = None
    preForm=FORM.none


class CardDamaged(Signal):
    senderCard=None
    receiverCard=None
    number=0
    isRangedAttack=False



class PlayerLPChanged(Signal):
    receiverPlayer:int=0

class PlayerLPLoseByBattle(PlayerLPChanged):
    senderCard:Card=None
    receiverPlayer:int=0
    lpLose=0

class PlayerLPLoseByEffect(PlayerLPChanged):
    receiverPlayer:int=0
    number=0

class PlayerLPRecover(PlayerLPChanged):
    receiverPlayer:int=0
    number=0



##############################Effect

class BeforeActivateEffect(Signal):
    isActively=False
    effect=None
    cardType=CARD_TYPE.none

class BeforeActivateEffectOnField(BeforeActivateEffect):
    isActively=False
    effect=None
    cardType=CARD_TYPE.none



class ActivateFinish(Signal):
    isActively=False

class ActivateMonsterEffectFinish(ActivateFinish):
    isActively=False

class ActivateSpellFinish(ActivateFinish):
    isActively=False

class ActivateTrapFinish(ActivateFinish):
    isActively=False


class ActivateCountered(Signal):
    effect=None


class EquipTo(Signal):
    equipSpell:Card=None
    monsterCard:Card=None

class EquipCancel(Signal):
    equipSpell:Card=None
    monsterCard:Card=None

class PlayerBuffChanged(Signal):
    side=0