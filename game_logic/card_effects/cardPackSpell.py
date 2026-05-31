# -*- coding: utf-8 -*-
from __future__ import annotations
from annos import *
from KBEDebug import *
from a import Signal
from b.Card import *
from a.Effect import *
from a.DuelConstants import *
from Constants import *



class Fusion(Card):
    # CARD_KEY="Fusion"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(Fusion_effect1)

class Fusion_effect1(Effect):
    effType = EFF_TYPE.active

    def y_cost(self,justCheck:bool,signal):
        #search the extra deck
        side=self.getSide()

        cardUidToCardGroups={}
        canSummonCardList=[]
        for extraMonster in self.game.extraDecks[side]:
            if extraMonster.cardType & CARD_TYPE.fusionMonster !=CARD_TYPE.fusionMonster:
                continue
            if extraMonster.settedMaterialFilter==None:
                continue
            #TODO 2v2
            if justCheck:
                searchLimit=1
            else:
                searchLimit=10000
            cardGroups=self.searchCardGroup(extraMonster.materialLocationMask, self.getSide(), CARD_TYPE.monster, extraMonster.materialMinNum, extraMonster.materialMaxNum, None, extraMonster.materialCardFilter, None, extraMonster.settedMaterialFilter, searchLimit)
            if cardGroups:
                if justCheck:
                    return True
                cardUidToCardGroups[extraMonster.uniID]=cardGroups
                canSummonCardList.append(extraMonster)

        if justCheck:#not found any
            return False

        if not canSummonCardList:
            return False

        summonCard=yield self.y_select1Card(canSummonCardList,TITLE.specialSummon,canCancel=True)
        if not summonCard:
            return False

        tributeGroups=cardUidToCardGroups[summonCard.uniID]
        tributeGroup=yield self.y_selectCardGroup(tributeGroups,TITLE.tribute,canCancel=True)
        if not tributeGroup:
            return False

        if summonCard.location!=LOCATION.extraDeck:
            return False


        self.saveTarget1(summonCard)
        self.saveTarget2(tributeGroup)

        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True

        summonCard=self.getLegalTarget1()
        if not summonCard:
            return False

        tributes=self.getLegalTarget2()
        if summonCard.settedMaterialFilter(tributes):
            pass
        else:
            #tributes illegal
            cardGroups=self.searchCardGroup(summonCard.materialLocationMask, self.getSide(), CARD_TYPE.monster, summonCard.materialMinNum, summonCard.materialMaxNum, None, summonCard.materialCardFilter, None, summonCard.settedMaterialFilter)
            if not cardGroups:
                return False
            tributes=yield self.y_selectCardGroup(cardGroups,TITLE.tribute,canCancel=False)
            if not tributes:
                return False

        tributeNum=len(tributes)
        successNum=yield self.y_tributeCard(tributes)
        if successNum!=tributeNum:
            return False

        sig=Signal.FusionSummon()
        sig.card=summonCard
        sig.tributes=tributes
        self.game.makeSignalReason(sig)

        yield self.y_specialSummon(summonCard,signal=sig)

        return True

class angel_wing(Card):
    CARD_KEY="angel wing"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(enemyDraw1)

class enemyDraw1(Effect):
    effType = EFF_TYPE.active

    AI_HINT = [AI_HINT.eraser]
    AI_POWER = 1
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True
        yield self.y_drawCard(self.getSide())
        return True


#[丢弃一张手牌,选对方场上一只怪兽]:破坏该怪兽
#[丢弃一张手牌]:破坏对方场上一只怪兽
class angel_wing_effect1(Effect):
    effType = EFF_TYPE.active
    manaCost = 0

    def y_cost(self,justCheck:bool,signal:Signal.Signal):
        cards=self.searchCards(LOCATION.hand,self.getSide(),CARD_TYPE.all)
        if self.owner in cards:
            cards.remove(self.owner)
        if not cards:
            return False

        enemyCards=self.game.searchCards(LOCATION.monsterZone,self.getEnemySideTuple(),CARD_TYPE.all,self)
        if not enemyCards:
            return False

        if justCheck:
            return True
        card=yield self.y_select1Card(cards,TITLE.sendToGrave,canCancel=True)
        if not card:
            return False
        successNum=yield self.y_sendCardToGrave(card)
        if successNum:
            pass
        else:
            return False

        enemyCard=yield self.y_select1Card(enemyCards,TITLE.destroy)
        if enemyCard:
            self.saveTarget1(enemyCard)
            return True
        return False


    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True

        DEBUG_MSG("use effect angel wing")

        enemyCard=self.getLegalTarget1()
        yield self.y_destroyCard(enemyCard)
        return True


class active_trap(Card):
    CARD_KEY="active_trap"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(active_trap_effect1)

class active_trap_effect1(Effect):
    effType = EFF_TYPE.active

    # observeSignals = (LOCATION.spellTrapZone,OBSERVESIGNAL_QUICK_EFFECT)

    AI_HINT = [AI_HINT.eraser]
    AI_POWER = 1
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        # if not self.isSignalQuickEffect(signal):
        #     return False

        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True
        DEBUG_MSG("activate trap")
        return True

#====================================



class AdditionalSummon(Card):
    # CARD_KEY="AdditionalSummon"
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(AdditionalSummon_effect1)
        self.initEffect(AdditionalSummon_effect2)

class AdditionalSummon_effect1(Effect):
    effType = EFF_TYPE.active

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 1
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True

        self.owner.setData("AdditionalSummonEffect1ActivateTurn",self.game.curTurn)
        return True

class AdditionalSummon_effect2(Effect):
    effType = EFF_TYPE.active

    activateLocation = LOCATION.grave
    observeSignals = (LOCATION.monsterZone,[Signal.NormalSummon])

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 1
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        turn=self.owner.getData("AdditionalSummonEffect1ActivateTurn")
        if turn:
            turn=int(turn)

        if turn==self.game.curTurn:
            return False
        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True
        return True


class m_rock(Card):
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(m_rock_effect1)

class m_rock_effect1(Effect):
    effType = EFF_TYPE.optionalInstant

    observeSignals = (LOCATION.monsterZone,[Signal.InBattle])

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 1

    def y_activate(self,justCheck:bool,signal:Signal.InBattle):
        if isSignal(signal,Signal.InBattle) and self.getSide() in signal.involvedSideList:
            pass
        else:
            return

        if justCheck:
            return True

        myCard:Card=signal.getMyCard(self.getSide())
        if not myCard or type(myCard)==int:
            return
        yield self.y_addCardData(myCard,1,1,effDuration=EFF_DURATION.utilBattleEnds)
        return True


class m_paper(Card):
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(m_paper_effect1)

class m_paper_effect1(Effect):
    effType = EFF_TYPE.optionalInstant

    observeSignals = (LOCATION.monsterZone,[Signal.InBattle])

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 1


    def y_activate(self,justCheck:bool,signal:Signal.InBattle):
        if isSignal(signal,Signal.InBattle) and self.getSide() in signal.involvedSideList:
            pass
        else:
            return
        if justCheck:
            return True

        #check enemy played scissors
        for effect in signal.activatedEffectList:
            if effect.owner.getName()=="m_scissors" and effect.getSide() in self.getEnemySideTuple():
                return False

        myCard:Card=signal.getMyCard(self.getSide())
        if not myCard:
            return
        if type(myCard)==int:
            myCard.setData("attackcancelled",str(signal.battleUniID))
            yield self.y_addPlayerShield()
        else:
            yield self.y_addShield(myCard,2,effDuration=EFF_DURATION.utilBattleEnds)
        return True


class m_scissors(Card):
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(m_scissors_effect1)

class m_scissors_effect1(Effect):
    effType = EFF_TYPE.optionalInstant

    observeSignals = (LOCATION.monsterZone,[Signal.InBattle])

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 1


    def y_activate(self,justCheck:bool,signal:Signal.InBattle):
        if isSignal(signal,Signal.InBattle) and self.getSide() in signal.involvedSideList:
            pass
        else:
            return

        if justCheck:
            return True

        enemyCard:Card=signal.getBattleEnemy(self.getSide())
        if not enemyCard or type(enemyCard)==int:
            return

        yield self.y_addCardData(enemyCard,-1,-1,effDuration=EFF_DURATION.utilBattleEnds)
        return True



######################bot spell card
class aisummon2monaters(Card):
    AUTHOR="Unnamed"
    def effectsInit(self):
        self.initEffect(aisummon2monaters_effect1)

class aisummon2monaters_effect1(Effect):
    effType = EFF_TYPE.active

    AI_HINT = [AI_HINT.eraser]
    EFF_POWER = 1
    def y_signal(self,signal):
        pass

    def y_cost(self,justCheck:bool,signal):
        if justCheck:
            return True
        return True

    def y_activate(self,justCheck:bool,signal):
        if justCheck:
            return True
        return True


