# from Handlers import *
from __future__ import annotations

import itertools

from KBEngine import *

from a.PlayerBuff import g_playerBuffClasses, PlayerBuff
from b.Card import *
from card_effects import shortEffects
from util import *
from annos import *
from a import Signal
from a import fitter
from a import CardBuff


class GameFunc:
    def __init__(self,game, duel):
        """
        duel: The Bridge between game logic and client
        game: Data Structures and game logic
        duelNode: contains functions of visual animations
        """
        self.duel: Duel = duel
        self.game: Game= game
        self.duelNode: DuelNode = self.duel.duelNode

    """
    sideOrTuple:
        0  self side,return (selfside,)
        -1  all side,return (1,2)
        1  return (1,0)
        (1,2) return (1,2)
        
    always return tuple 
    
    """
    def _parseSide(self, sideOrTuple:Union[int,Tuple[int]])->Tuple[int]:
        if sideOrTuple==0:
            getSide=getattr(self,"getSide",None)
            if getSide:
                return (getSide(),)
        elif type(sideOrTuple)==tuple:
            return sideOrTuple
        elif type(sideOrTuple)==int:
            if sideOrTuple<0:
                return tuple(self.game.monsters.keys())
            elif sideOrTuple in self.game.monsters:
                return (sideOrTuple,)
        ERROR_MSG("_parseSide error ",sideOrTuple)
        return (tuple(self.game.monsters.keys())[0],)

    # def _arrangeCardList(self,cardList):
    #     if type(cardList)==tuple:
    #         cardList=list(cardList)
    #     #enemy first
    #     cardList.sort(key=lambda card: (
    #         card.side == self.game.whoseTurn,
    #         card.location,
    #     ))
    #     return cardList



    def __________________query(self):
        pass

    """
    search cards match the filterFunc,return list of results
    
    def filterFunc(card):
        if card satisfied:
            return True
            
    affectSource: If the effect will affect the target card, then pass the effect.If the effect will not affect the card,then pass "None"
    """

    def search1Card(self, locationMask, sideOrTuple: Union[int, tuple], cardTypeMask=CARD_TYPE.all, affectSource:Effect=None, filterFunc=None) -> \
            Union[Card, None]:
        foundCards = self.searchCards(locationMask, sideOrTuple, cardTypeMask, affectSource, filterFunc, 1)
        if len(foundCards):
            return foundCards[0]
        return None

    """
    search cards match the basicFilter,return list of results
    
    def filterFunc(card):
        if card satisfied:
            return True
    
    """

    def searchCards(self, locationMask, sideOrTuple: Union[int, tuple] = -1, cardTypeMask=CARD_TYPE.all, affectSource:Effect=None, filterFunc=None,
                    maxFoundNum=10000) -> [Card]:
        game=self.game
        allCards = []

        sideOrTuple=self._parseSide(sideOrTuple)

        for side in sideOrTuple:
            if locationMask & LOCATION.monsterZone:
                allCards += game.monsters[side]
            if locationMask & LOCATION.spellTrapZone:
                allCards += game.spells[side]
            if locationMask & LOCATION.hand:
                allCards += game.hands[side]
            if locationMask & LOCATION.deck:
                allCards += game.decks[side]
            if locationMask & LOCATION.grave:
                allCards += game.graves[side]
            if locationMask & LOCATION.extraDeck:
                allCards += game.extraDecks[side]
            if locationMask & LOCATION.banish:
                allCards += game.banishes[side]

        if not allCards:
            return []

        result = []
        for card in allCards:
            if card.cardType & cardTypeMask == 0:
                continue
            if filterFunc and not filterFunc(card):
                continue
            result.append(card)
            if len(result) >= maxFoundNum:
                return result

        if affectSource:
            result=affectSource.removeNotAffectedInList(result)
        return result


    """
    search card groups match the filters,return list of groups
    
    locationMask: LOCATION.banish|LOCATION.grave , search banished and grave
    sideOrTuple :  1 or (1,2) or 0
    cardTypeMask: CARD_TYPE.monster|CARD_TYPE.spell ,any monster and spell
    minNum,maxNum: the min and max number of cards in group, if -1, =len(filterList) 
    basicFilter: function(Card)   all cards filter first
    preGroupFilter: function([Card])  pre filter,to remove obviously impossible groups ,improve performance
    groupFilter: function([Card]) filter of the group,ignore card order
    maxSearchNum:the max number of search results
    """

    def searchCardGroup(self, locationMask, sideOrTuple, cardTypeMask=CARD_TYPE.all, minNum=1, maxNum=1, affectSource:Effect=None, basicFilter=None,
                        preGroupFilter=None, groupFilter=None, maxSearchNum=10000) -> [[Card]]:
        if minNum > maxNum != 0:
            ERROR_MSG("findCardGroups minNum>maxNum")
            return []

        if minNum < 0:
            minNum = 0
        if minNum == maxNum == 0:
            return []

        allCards = self.searchCards(locationMask, sideOrTuple, cardTypeMask, affectSource, basicFilter)
        lenAllCards = len(allCards)
        if not lenAllCards:
            return []

        if minNum > lenAllCards:
            return []

        if maxSearchNum < 0:
            maxSearchNum = 10000

        returnResult = []
        if maxNum < 0:
            num2 = lenAllCards
        else:
            num2 = min(maxNum, lenAllCards)

        cnt = 0
        for r in range(minNum, num2 + 1):
            for group in itertools.combinations(allCards, r):
                if not preGroupFilter or preGroupFilter(group):
                    for g in itertools.permutations(group):  #try (1,2,3),(1,3,2),...
                        cnt += 1
                        if not groupFilter or groupFilter(g):
                            returnResult.append(group)
                            break
                    if len(returnResult) >= maxSearchNum or cnt > 5000000:
                        if maxSearchNum >= 10000 or cnt > 5000000:
                            ERROR_MSG("searchCardGroup too many results,may use searchCards instead:",
                                      self.game.getCurrentCardName())
                        return returnResult

        return returnResult

    def __________________queryEnd(self):
        pass


    def _____________selector(self):
        pass


    #result == 0 or 1 , 0 is Yes
    def y_showYesNoPopUp(self,  title, text,side=0)->int:
        side=self._parseSide(side)[0]
        if side==0:
            ERROR_MSG("y_showYesNoPopUp sideerror ",side)
            return 1

        result = yield self.duel.y_showPopup(title, text, side, ["YES"], 1,"NO")
        return result


    # return 0:the first option 1:the secound
    def y_showOptionsPopUp(self,title,text,side,options:List[str],defaultResult:int=0,canCancel=False)->int:
        side=self._parseSide(side)[0]
        cancelOption=""
        if canCancel:
            cancelOption="CANCEL"

        result=yield self.duel.y_showPopup(title,text,side,options,defaultResult,cancelOption)
        return result


    """
    request player to choose 1 card from cardList,return the chosen card
    """

    def y_select1Card(self,  cardList: [Card], title:str,side: int=0,defaultResult: Card = None, canCancel=False) -> Card:
        if defaultResult != None:
            defaultResult = [defaultResult]
        result = yield self.y_selectCards(cardList, title, side, 1, 1, defaultResult, canCancel)
        if not result or result == []:
            return None
        return result[0]


    """
    request player to choose cards from cardList
    
    side: 1 or 2
    defaultResult: the best result the bot chooses
    canCancel:if True,play can cancel and return None,if False,player cant cancel and return defaultResult if timeout
    
    usage:
        chosenCard = yield y_chooseCard(1,[card1,card2],card1,True)
    """

    def y_selectCards(self, cardList: [Card],title: str,side: int =0, minNum: int=1, maxNum: int=1,
                      defaultResultList: [Card] = None, canCancel=False, hasOrder=False) -> [Card]:
        side=self._parseSide(side)[0]
        if len(cardList) == 0:
            return []

        cardList = list(set(cardList))


        if maxNum == minNum == 1:
            isOneCardCanLaser = True
            for card in cardList:
                if card.isMonsterOnField() or ((card.location == LOCATION.hand or card.location == LOCATION.spellTrapZone) and card.side == side):
                    pass
                else:
                    isOneCardCanLaser = False
                    break
        else:
            isOneCardCanLaser = False


        resultList=[]
        if isOneCardCanLaser:
            result = yield self.duel.y_showFieldHandSelector(cardList,title,side, defaultResultList, canCancel)
            if result:
                resultList=[result]
            else:
                resultList= None
        else:
            options = ["OK"]
            defaultOption = 0
            cancelOption=""
            if canCancel:
                cancelOption=  "CANCEL"

            option, resultList = yield self.duel.y_showCardSelectorPanel(cardList,title,side, options , minNum, maxNum,
                                                                         defaultOption, defaultResultList, cancelOption,
                                                                         hasOrder)
            if option==1:
                resultList=None

        # if title==TITLE.specialSummon and resultList and 0<len(resultList)<10:
        #     shouldCancel=yield self.game.y_checkHasNotAffordableEffect(side,resultList,Signal.SpecialSummon())
        #     if shouldCancel:
        #         resultList=yield self.y_selectCards(cardList,title,side, minNum, maxNum,defaultResultList, canCancel, hasOrder)
        return resultList


    """
    if cancel ,return None
    """
    def y_selectCardGroup(self, cardGroups: List[List[Card]],title,side:int=0,bestGroup: [Card] = None, canCancel=False) -> \
            Union[None,List[Card]]:
        side=self._parseSide(side)[0]
        if not cardGroups:
            if canCancel:
                return None
            else:
                return []

        cardList = groupsToList(cardGroups)

        isOneCardCanLaser = True
        cancelReturnEmpty = False
        minNum = 999999
        maxNum = 0
        for i in range(len(cardGroups) - 1, -1, -1):
            group = cardGroups[i]
            lenGroup = len(group)
            if lenGroup < minNum:
                minNum = lenGroup
            if lenGroup > maxNum:
                maxNum = lenGroup

            if lenGroup > 1:
                isOneCardCanLaser = False
            elif lenGroup == 0:
                canCancel = True
                cancelReturnEmpty = True
            elif isOneCardCanLaser:
                for card in group:
                    if card.isMonsterOnField() or ((card.location == LOCATION.hand or card.location == LOCATION.spellTrapZone) and card.side == side):
                        pass
                    else:
                        isOneCardCanLaser = False
                        break
            if not isOneCardCanLaser:
                break


        resultList=[]
        if isOneCardCanLaser:
            if not len(cardList):
                return []
            if not bestGroup:
                defaultCard = None
            else:
                defaultCard = bestGroup[0]
            result = yield self.duel.y_showFieldHandSelector(cardList,title,side, defaultCard, canCancel)
            if result:
                resultList= [result]
            else:
                if cancelReturnEmpty:
                    resultList= []
                else:
                    resultList= None
        else:
            options = ["OK"]
            cancelOption=""
            if canCancel:
                cancelOption= "CANCEL"
            option, resultList = yield self.duel.y_showCardSelectorPanel(cardList,title,side, options, minNum, maxNum,
                                                                         0, bestGroup, cancelOption,
                                                                         legalGroups=cardGroups)
            if option == 1:
                resultList=None

        # if title==TITLE.specialSummon and resultList and 0<len(resultList)<10:
        #     shouldCancel=yield self.game.y_checkHasNotAffordableEffect(side,resultList,Signal.SpecialSummon())
        #     if shouldCancel:
        #         resultList=yield self.y_selectCardGroup(cardGroups,title,side,bestGroup, canCancel)
        return resultList


    def ___________________selectorEnd(self):
        pass


    def y_drawCard(self, sideOrTuple:Union[int,Tuple]=0, drawNum=1, isDrawPhaseDraw=False)->List[Card]:
        sideOrTuple=self._parseSide(sideOrTuple)

        game=self.game
        signals=[]
        cards=[]
        for side in sideOrTuple:
            #draw anim
            drawAnim=AVATAR_ANIM.drawCard
            if isDrawPhaseDraw and randPercent(0.1):
                drawAnim=AVATAR_ANIM.drawCardK
            self.duelNode.playanimAvatarAnim(side,drawAnim)

            for i in range(drawNum):
                if len(game.decks[side])>0:
                    card = game.decks[side][-1]
                    self.duelNode.playanimPlayerAddCardToHand(side, CardData.getNone(),True,False,True)
                    t=yield game._y_changeCardLocation(card, LOCATION.hand, side, enterListAnim=ANIM.drawCard)
                    signals.extend(t)
                    cards.append(card)
                else:
                    self.duel.setLoser(side,LOSE_REASON.noCardToDraw)

        if not isDrawPhaseDraw:
            sig=Signal.DrawCardsByEffect()
            sig.cardList=cards
            sig.sideTuple=sideOrTuple
            game.makeSignalReason(sig)
            signals.append(sig)

        for signal in signals:
            yield game.y_sendSignal(signal)

        return cards


    def y_setCardFromDeck(self,sideOrTuple:Union[int,Tuple]=0, drawNum=1):
        pass


    def y_changeToBattlePhaseByEffect(self):
        if self.game.phase==PHASE.mainphase1:
            yield self.game.y_changePhase()

    def y_changeToMainPhase2ByEffect(self):
        if self.game.phase==PHASE.battle:
            yield self.game.y_changePhase()


    def y_turnEndsByEffect(self):
        result=yield self.game.y_turnEnds()
        return result

    def _________________________basicOperates(self):
        pass

    """
    if receiver is int type,attacks player
    """
    def y_battleByEffect(self,attacker:Card,receiver:Union[Card,int]):
        if type(receiver)!=int:
            isBattled=yield self.game.y_battle(attacker,receiver,False)
        else:
            isBattled=yield self.game.y_directAttack(attacker,receiver,False)
        return isBattled

    def y_counterEffectActivate(self, signal:Signal.BeforeActivateEffect):
        game=self.game
        if not isSignal(signal,Signal.BeforeActivateEffect):
            ERROR_MSG("y_counterEffectActivate can only used in signal BeforeActivateEffect")
            return False
        effect=signal.effect
        cardOrList=[effect.owner]
        effPeriod,dealingEff=game.getDealingEffect()
        if dealingEff:
            cardOrList=dealingEff.removeNotAffectedInList(cardOrList)

        if cardOrList:
            effect.addFlagCount(EFF_FLAG.activateCountered)
            sig=Signal.ActivateCountered()
            sig.effect=effect
            sig.card=effect.owner
            game.makeSignalReason(sig)
            yield game.y_sendSignal(sig)
            return True
        return False


    def y_silenceCard(self,cardOrList,effDuration=EFF_DURATION.onceForever, uniqueSourceID:int=0):
        result=yield self.y_addCardBuff(cardOrList,CARD_BUFF.silenced,effDuration,uniqueSourceID)
        return result


    def y_addImmunityBuffToCard(self, cardOrList,immunityMask:IMMUNITY_MASK, effDuration=EFF_DURATION.onceForever, uniqueSourceID:int=0):
        cardBuff=CardBuff.immunity()
        cardBuff.immunityMask=immunityMask
        result=yield self.y_addCardBuff(cardOrList,cardBuff,effDuration,uniqueSourceID)
        return result



    def y_addCardBuff(self, cardOrList:Union[Card,List[Card]], buffIDOrCardBuff:Union[CARD_BUFF,CardBuff], effDuration=EFF_DURATION.onceForever, uniqueSourceID:int=0):
        if not cardOrList:
            return
        if type(cardOrList) != list:
            cardOrList = [cardOrList]

        cardBuff=None
        if type(buffIDOrCardBuff)==int:
            if buffIDOrCardBuff not in CardBuff.g_buffClasses:
                ERROR_MSG(f"y_addCardBuff buffID {buffIDOrCardBuff} not defined in CardBuff.py")
                return

            if buffIDOrCardBuff < 10000:
                ERROR_MSG(f"buffID {buffIDOrCardBuff} has specified method,dont use y_addCardBuff")
                return
            cardBuff=CardBuff.g_buffClasses[buffIDOrCardBuff]()
        elif type(buffIDOrCardBuff) is type:
            ERROR_MSG("y_addCardBuff buffIDOrCardBuff is type")
            return
        else:
            cardBuff=buffIDOrCardBuff

        cardBuff.duration=effDuration
        cardBuff.uniqueSourceID=uniqueSourceID

        game=self.game

        if effDuration!=EFF_DURATION.fromSource:
            effPeriod,effect=game.getDealingEffect()
            if effect:
                cardOrList=effect.removeNotAffectedInList(cardOrList)

        shouldCopy=len(cardOrList)>1

        signals=[]
        paraID=game.genUniID()
        for card in cardOrList:
            if shouldCopy:
                tempCardBuff=copy.copy(cardBuff)
            else:
                tempCardBuff=cardBuff

            if card._addBuff(tempCardBuff):
                fx=tempCardBuff.fxID
            else:
                fx=FX_ID.none
            game.appendSignalsByBuffID(signals, tempCardBuff.BUFF_ID, card)
            card.recalBuffsAndOnDataChanged(fx, paraID=paraID)

        for signal in signals:
            game.makeSignalReason(signal)
            yield game.y_sendSignal(signal)


    def y_changeCardData(self, cardOrList:Union[Card,List[Card]], newAtk:int=None, newDefence:int=None, newRangeAtk:int=None, newLevel=None, newAttr:ATTR=None, newRace:RACE=None, newAttackTimes:int=None, effDuration=EFF_DURATION.onceForever, uniqueSourceID:int=0):
        if not cardOrList:
            return
        if type(cardOrList) != list:
            cardOrList = [cardOrList]

        game=self.game

        if effDuration!=EFF_DURATION.fromSource:
            effPeriod,effect=game.getDealingEffect()
            if effect:
                cardOrList=effect.removeNotAffectedInList(cardOrList)

        signals=[]
        paraID=game.genUniID()
        fx=FX_ID.none
        for card in cardOrList:
            tempSignals=[]
            if 0:card=card #type:Card
            if newAtk!=None and card.atk!=ATK.none:
                if newAtk>=card.atk:
                    fx=FX_ID.addAtk
                else:
                    fx=FX_ID.reduceAtk

                b=CardBuff.attackChange(effDuration, uniqueSourceID)
                b.number=newAtk
                if not card._addBuff(b):
                    fx=FX_ID.none
                game.appendSignalsByBuffID(tempSignals, b.BUFF_ID, card)

            if newRangeAtk!=None and card.rangeAtk!=ATK.none:
                if newRangeAtk>=card.rangeAtk:
                    fx=FX_ID.addAtk
                else:
                    fx=FX_ID.reduceAtk
                b=CardBuff.rangeAtkChange(effDuration, uniqueSourceID)
                b.number=newRangeAtk
                if not card._addBuff(b):
                    fx=FX_ID.none
                game.appendSignalsByBuffID(tempSignals, b.BUFF_ID, card)

            if newDefence!=None and card.defence!=ATK.none:
                if newDefence>=card.defence:
                    fx=FX_ID.addShield
                else:
                    fx=FX_ID.reduceAtk
                b=CardBuff.defenceChange(effDuration, uniqueSourceID)
                b.number=newDefence
                if not card._addBuff(b):
                    fx=FX_ID.none
                game.appendSignalsByBuffID(tempSignals, b.BUFF_ID, card)

            if newLevel!=None:
                if newLevel>=card.level:
                    fx=FX_ID.addLV
                else:
                    fx=FX_ID.reduceLV
                b=CardBuff.levelChange(effDuration, uniqueSourceID)
                b.number=newLevel
                if not card._addBuff(b):
                    fx=FX_ID.none
                game.appendSignalsByBuffID(tempSignals, b.BUFF_ID, card)

            if newAttr!=None:
                b=CardBuff.attrChange(effDuration, uniqueSourceID)
                b.newAttr=newAttr
                if not card._addBuff(b):
                    fx=FX_ID.none
                game.appendSignalsByBuffID(tempSignals, b.BUFF_ID, card)
                fx=FX_ID.changeData

            if newRace!=None:
                b=CardBuff.raceChange(effDuration, uniqueSourceID)
                b.newRace=newRace
                if not card._addBuff(b):
                    fx=FX_ID.none
                game.appendSignalsByBuffID(tempSignals, b.BUFF_ID, card)
                fx=FX_ID.changeData

            if newAttackTimes!=None:
                b=CardBuff.attackTimesChange(effDuration, uniqueSourceID)
                b.number=newAttackTimes
                if not card._addBuff(b):
                    fx=FX_ID.none
                fx=FX_ID.changeData

            signals.extend(game.makeSignalsNoDuplicate(tempSignals))
            card.recalBuffsAndOnDataChanged(fx, paraID=paraID)

        for signal in signals:
            game.makeSignalReason(signal)
            yield game.y_sendSignal(signal)


    def y_addCardData(self, cardOrList:Union[Card,List[Card]], attackAdd:int=None, defenceAdd:int=None, rangeAtkAdd:int=None, levelAdd:int=None, attackTimesAdd:int=None, effDuration=EFF_DURATION.onceForever, uniqueSourceID:int=0, fx:FX_ID=0):
        if not cardOrList:
            return
        if type(cardOrList) != list:
            cardOrList = [cardOrList]

        game=self.game

        if effDuration!=EFF_DURATION.fromSource:
            effPeriod,effect=game.getDealingEffect()
            if effect:
                cardOrList=effect.removeNotAffectedInList(cardOrList)

        signals=[]
        paraID=game.genUniID()
        for card in cardOrList:
            tempSignals=[]
            if 0:card=card #type:Card
            if attackAdd!=None and card.atk!=ATK.none:
                if not fx:
                    if attackAdd>=0:
                        fx=FX_ID.addAtk
                    else:
                        fx=FX_ID.reduceAtk
                b=CardBuff.attackAdd(effDuration, uniqueSourceID)
                b.number=attackAdd
                if not card._addBuff(b):
                    fx=FX_ID.none
                game.appendSignalsByBuffID(tempSignals, b.BUFF_ID, card)

            if rangeAtkAdd!=None and card.rangeAtk!=ATK.none:
                if not fx:
                    if rangeAtkAdd>=0:
                        fx=FX_ID.addAtk
                    else:
                        fx=FX_ID.reduceAtk
                b=CardBuff.rangeAtkAdd(effDuration, uniqueSourceID)
                b.number=rangeAtkAdd
                if not card._addBuff(b):
                    fx=FX_ID.none
                game.appendSignalsByBuffID(tempSignals, b.BUFF_ID, card)

            if defenceAdd!=None and card.defence!=ATK.none:
                if not fx:
                    if defenceAdd>=0:
                        fx=FX_ID.addShield
                    else:
                        fx=FX_ID.reduceAtk
                b=CardBuff.defenceAdd(effDuration, uniqueSourceID)
                b.number=defenceAdd
                if not card._addBuff(b):
                    fx=FX_ID.none
                game.appendSignalsByBuffID(tempSignals, b.BUFF_ID, card)

            if levelAdd!=None:
                if not fx:
                    if levelAdd>=0:
                        fx=FX_ID.addLV
                    else:
                        fx=FX_ID.reduceLV
                b=CardBuff.levelAdd(effDuration, uniqueSourceID)
                b.number=levelAdd
                if not card._addBuff(b):
                    fx=FX_ID.none
                game.appendSignalsByBuffID(tempSignals, b.BUFF_ID, card)

            if attackTimesAdd!=None:
                if not fx:
                    fx=FX_ID.addLV
                b=CardBuff.attackTimesAdd(effDuration, uniqueSourceID)
                b.number=attackTimesAdd
                if not card._addBuff(b):
                    fx=FX_ID.none

            signals.extend(game.makeSignalsNoDuplicate(tempSignals))

            card.recalBuffsAndOnDataChanged(fx,paraID)

        for signal in signals:
            game.makeSignalReason(signal)
            yield game.y_sendSignal(signal)



    def y_multiplyCardData(self, cardOrList:Union[Card,List[Card]], attackMulti:float=None, rangeAtkMulti:float=None, defenceMulti:float=None, effDuration=EFF_DURATION.onceForever, sourceID:int=0):
        if not cardOrList:
            return
        if type(cardOrList) != list:
            cardOrList = [cardOrList]

        game=self.game

        if effDuration!=EFF_DURATION.fromSource:
            effPeriod,effect=game.getDealingEffect()
            if effect:
                cardOrList=effect.removeNotAffectedInList(cardOrList)

        signals=[]
        paraID=game.genUniID()
        fx=FX_ID.none
        for card in cardOrList:
            tempSignals=[]
            if 0:card=card #type:Card
            if attackMulti!=None and card.atk!=ATK.none:
                if attackMulti>=1:
                    fx=FX_ID.addAtk
                else:
                    fx=FX_ID.reduceAtk
                b=CardBuff.attackMulti(effDuration,sourceID)
                b.number=attackMulti
                if not card._addBuff(b):
                    fx=FX_ID.none
                game.appendSignalsByBuffID(tempSignals, b.BUFF_ID, card)

            if rangeAtkMulti!=None and card.rangeAtk!=ATK.none:
                if rangeAtkMulti>=0:
                    fx=FX_ID.addAtk
                else:
                    fx=FX_ID.reduceAtk
                b=CardBuff.rangeAtkMulti(effDuration,sourceID)
                b.number=rangeAtkMulti
                if not card._addBuff(b):
                    fx=FX_ID.none
                game.appendSignalsByBuffID(tempSignals, b.BUFF_ID, card)

            if defenceMulti!=None and card.defence!=ATK.none:
                if defenceMulti>=1:
                    fx=FX_ID.addShield
                else:
                    fx=FX_ID.reduceAtk
                b=CardBuff.defenceMulti(effDuration,sourceID)
                b.number=defenceMulti
                if not card._addBuff(b):
                    fx=FX_ID.none
                game.appendSignalsByBuffID(tempSignals, b.BUFF_ID, card)

            signals.extend(game.makeSignalsNoDuplicate(tempSignals))
            card.recalBuffsAndOnDataChanged(fx, paraID=paraID)

        for signal in signals:
            game.makeSignalReason(signal)
            yield game.y_sendSignal(signal)


    def y_removeBuffEffectSource(self, cardOrList:Union[Card, List[Card]],sourceID):
        game=self.game
        if not cardOrList:
            return
        if type(cardOrList) != list:
            cardOrList = [cardOrList]

        removeChangeControllerMonsters=[]
        signals=[]
        for card in cardOrList:
            removedBuffs=card._removeBuffBySource(sourceID)
            if removedBuffs:
                tempSignals=[]
                for buff in removedBuffs:
                    if buff.BUFF_ID==CARD_BUFF.controlled:
                        removeChangeControllerMonsters.append(card)
                    game.appendSignalsByBuffID(tempSignals, buff.BUFF_ID, card)
                signals.extend(game.makeSignalsNoDuplicate(tempSignals))
                card.recalBuffsAndOnDataChanged(FX_ID.none)

        for signal in signals:
            game.makeSignalReason(signal)
            yield game.y_sendSignal(signal)

        for monster in removeChangeControllerMonsters:
            if not monster.hasBuff(CARD_BUFF.controlled):
                yield self.y_changeMonsterController(monster,monster.side_0,isByEffect=False)



    def y_addPlayerBuff(self, sideOrTuple, playerBuffID:PLAYER_BUFF, effDuration=EFF_DURATION.onceForever, sourceID=0):
        game=self.game
        sideOrTuple=game._parseSide(sideOrTuple)
        sigs=[]
        for side in sideOrTuple:
            if playerBuffID in g_playerBuffClasses:
                buff=g_playerBuffClasses[playerBuffID](effDuration,sourceID)
            else:
                buff=PlayerBuff(effDuration,sourceID)
            buff.BUFF_ID=playerBuffID
            buff.side=side
            buff.addTurn=game.curTurn
            game.playerBuffs[side].append(buff)
            game.recalPlayerBuff(side)
            sig=Signal.PlayerBuffChanged()
            sig.side=side
            sigs.append(sig)

        for signal in sigs:
            game.makeSignalReason(signal)
            yield game.y_sendSignal(signal)



    def y_removePlayerBuffEffectSource(self,sideOrTuple,sourceID):
        game=self.game
        sideOrTuple=game._parseSide(sideOrTuple)
        sigs=[]
        for side in sideOrTuple:
            buffList=game.playerBuffs[side]
            deled=False
            for i in range(len(buffList)-1,-1,-1):
                b:PlayerBuff=buffList[i]
                if b.sourceID==sourceID:
                    del buffList[i]
                    deled=True
            if deled:
                sig=Signal.PlayerBuffChanged()
                sig.side=side
                sigs.append(sig)
        for sig in sigs:
            game.makeSignalReason(sig)
            yield game.y_sendSignal(sig)


    def y_cardAddShortEffect(self, card, shortEffectName, data="", effDuration=EFF_DURATION.onceForever, sourceID=0):
        """
        Dynamically grant a named short effect (see shortEffects.py) to a card at runtime.

        The grant rides the buff system: a CardBuff.ShortEffectBuff is added via
        y_addCardBuff, and Card._recalBuffs reconciliation creates/tears down the actual
        Effect. So the short effect honours every EFF_DURATION (utilTurnEnds,
        utilMyTurnEnds, utilBattleEnds, ...) and disappears exactly like a buff, and can
        be removed with y_removeCardBuffBySource(sourceID).

        Parameters
        ----------
        card            : the Card that should gain the short effect
        shortEffectName : g_shortEffects registry key, e.g. 'Pierce' / 'Evasion'.
                          A ShortEffect subclass is also accepted (its class name is used).
        data            : single argument carrier — pass the number for NEED_NUM effects
                          (e.g. data=2 for Slow) or the string for ':' data effects; read
                          back on the effect via getShortEffectTailNumber() (int(self.data)).
        effDuration     : EFF_DURATION for the grant; fully handled by the buff machinery.
        sourceID        : uniqueSourceID of the grant buff; pass non-zero to allow later
                          removal by source. NOTE: one sourceID maps to one grant slot, so
                          granting two different short effects under the same non-zero
                          sourceID will replace rather than stack — use distinct ids.

        Returns
        -------
        The active Effect for this short effect, or None if it was not added (e.g. immune).
        """
        if not card:
            return None

        # Accept a ShortEffect subclass as well as a registry-key string
        if not isinstance(shortEffectName, str):
            shortEffectName = shortEffectName.__name__

        name = shortEffectName

        if name not in g_shortEffects:
            ERROR_MSG("y_cardAddShortEffect not recognize shortEffect ", name, card.getName())
            return None

        ShortEffClass = g_shortEffects[name]

        data = str(data) if data != "" else ""
        if getattr(ShortEffClass, "NEED_NUM", False) and not data:
            ERROR_MSG(f"{card.getName()} shortEffect {name} needs a data argument")
            data = "1"

        # Add the grant buff; y_addCardBuff applies immunity filtering, duration/sourceID,
        # and triggers _recalBuffs -> reconciliation which connects the short effect
        buff = CardBuff.ShortEffectBuff(name, data)
        yield self.y_addCardBuff(card, buff, effDuration, sourceID)

        return card.getEffect(ShortEffClass)


    def y_damageCard(self,cardOrList: Union[Card, List[Card]],damageNumber:int,damageFX=FX_ID.effectDamage,rangedAttacker:Card=None,paraID=0):
        if not cardOrList:
            return 0
        if type(cardOrList) != list:
            cardOrList = [cardOrList]

        game=self.game

        effPeriod,effect=game.getDealingEffect()
        if effect:
            cardOrList=effect.removeNotAffectedInList(cardOrList)


        changeDataSignals=[]
        damageSignals=[]
        changePlaceSignals=[]
        destroySignals=[]
        dieList=[]
        successNum=0
        if paraID==0:
            paraID=game.genUniID()
        for card in cardOrList:
            if not card.canBeDamage():
                continue
            successNum+=1

            shouldBroken=False
            shouldDie=card.checkShouldDieTakeDamage(damageNumber)
            if not shouldDie:
                tempSignals=card.takeDamageBuff(damageNumber)
                changeDataSignals.extend(tempSignals)
                if not card.hasLife():
                    shouldBroken=True


            sig=Signal.CardDamaged(card)
            sig.receiverCard=card
            sig.number=damageNumber
            if rangedAttacker:
                sig.senderCard=rangedAttacker
                sig.isRangedAttack=True
            elif effect:
                sig.senderCard=effect.owner
            damageSignals.append(sig)


            shouldPlayAnim=False
            if card.location&LOCATION.mask_onField:
                shouldPlayAnim=True
            if card.defence>0:
                anim=ANIM.none
            else:
                anim=ANIM.animDie
                shouldPlayAnim=True

            if shouldPlayAnim:
                en=card.getCardEntity()
                if not rangedAttacker:
                    fromCard=None
                    if effect:
                        fromCard=effect.owner
                    if effect and effect.getClassName()=="Resistance":
                        card.playanimFx(FX_ID.addShield,paraID=paraID)
                    card.playanimFx(damageFX,anim,damageNumber,NUMBER_TYPE.damageCard,fromCard,paraID=paraID)
                elif en!=None: #ranged
                    en.c_cardData=card
                    battleResult=BattleResult()
                    battleResult.battleResultAnim=ANIM.getHit
                    battleResult.otherEntityID=rangedAttacker.entityID
                    battleResult.hitFx=FX_ID.beHit
                    battleResult.number=damageNumber
                    battleResult.numberType:NUMBER_TYPE=NUMBER_TYPE.damageCard
                    battleResult.shouldBroken=shouldBroken
                    battleResult.shouldDie=shouldDie
                    en.playanimBattleResult(battleResult,paraID)
                elif en==None:
                    ERROR_MSG("damage card but no entity ",card.getName())
            if shouldDie:
                dieList.append(card)

        for card in dieList:
            t=yield game._y_changeCardLocation(card, LOCATION.grave, card.side_0)
            changePlaceSignals.extend(t)

            sig=Signal.Destroyed(card)
            game.makeSignalReason(sig)
            destroySignals.append(sig)

        for signal in changeDataSignals:
            yield game.y_sendSignal(signal)
        for signal in damageSignals:
            yield game.y_sendSignal(signal)
        for signal in changePlaceSignals:
            yield game.y_sendSignal(signal)
        for signal in destroySignals:
            yield game.y_sendSignal(signal)

        return successNum

    def y_healCard(self,cardOrList: Union[Card, List[Card]],healNumber,healFx=FX_ID.recoverHP,paraID=0):
        successNum=yield self.y_damageCard(cardOrList,-healNumber,healFx,paraID=paraID)
        return successNum


    def y_tributeCard(self, cardOrList:Union[Card, List[Card]],fxID=FX_ID.sacrificeCircle,dieAnim=ANIM.fallInGround,toSummonCard:Card=None) -> int:
        if not cardOrList:
            return 0
        if type(cardOrList) != list:
            cardOrList = [cardOrList]

        game=self.game

        effPeriod,effect=game.getDealingEffect()

        refugeList=[]
        if toSummonCard==None:
            if effect:
                cardOrList=effect.removeNotAffectedInList(cardOrList)

                refugeList=yield self._y_dealBeforeRemovedSignal(cardOrList,"tribute")


        changePlaceSigs=[]
        tributeSigs=[]
        dieList=[]

        paraID = game.genUniID()
        successNum = 0
        for card in cardOrList:
            if card in refugeList:
                self.duelNode.playanimFxOnRemovedCard(card.uniID,fxID,paraID)
                continue

            if not card.canTribute():
                continue

            successNum += 1
            shouldDie=True

            if toSummonCard==None:
                if effect and effect.hasFlagCount(EFF_FLAG.resistFromRemovedByEffect, card):
                    effect.reduceFlagCount(EFF_FLAG.resistFromRemovedByEffect, card)
                    dieAnim=ANIM.getHit
                    shouldDie=False

            card.playanimFx(fxID, dieAnim, paraID=paraID)

            if shouldDie:
                dieList.append(card)


        for card in dieList:
            signal = Signal.Tributed(card)
            if toSummonCard==None:
                game.makeSignalReason(signal)
            else:
                signal.reasonEffect=None
                signal.reasonCard=toSummonCard
            tributeSigs.append(signal)

            if card.isInHand():
                self.duelNode.playanimPlayerDiscard1Card(card.side, card)
            elif card.isInDeck():
                self.duelNode.playanimPlayerDeckRemove1Card(card.side,card)

            t=yield game._y_changeCardLocation(card, LOCATION.grave)
            changePlaceSigs.extend(t)


        for signal in changePlaceSigs:
            yield game.y_sendSignal(signal)

        for signal in tributeSigs:
            yield game.y_sendSignal(signal)

        return successNum

    def y_changeForm(self, cardOrList: Union[Card, List[Card]], newForm: FORM=FORM.none, isByEffect=True):
        game=self.game
        if not cardOrList:
            return
        if type(cardOrList) != list:
            cardOrList = [cardOrList]

        if newForm not in (FORM.none,FORM.attack,FORM.defence,FORM.defenceSet):
            ERROR_MSG("newForm not in (FORM.none,FORM.attack,FORM.defence,FORM.defenceSet) :",newForm)
            return

        if isByEffect:
            effPeriod,effect=game.getDealingEffect()
            if effect:
                cardOrList=effect.removeNotAffectedInList(cardOrList)

        successNum=0
        signals=[]
        paraID=game.genUniID()
        for card in cardOrList:
            if newForm==FORM.none:
                newForm=FORM.attack
                if card.form==FORM.attack:
                    newForm=FORM.defence
            if card.defence==ATK.none:
                newForm=FORM.attack
            if newForm==FORM.attack:
                anim=ANIM.changeToAttack
            elif newForm==FORM.defence:
                anim=ANIM.changeToDefence
            elif newForm==FORM.defenceSet:
                ERROR_MSG("defence set not implemented")
                continue
            else:
                ERROR_MSG("monster form error ",newForm)
                continue

            card.cantChangeFormThisTurn=True

            if card.form==newForm:
                successNum+=1
                continue

            if card.canChangeForm(newForm):
                successNum+=1
                preForm=card.form
                card.form=newForm

                card.playanimFx(FX_ID.none,anim,paraID=paraID)

                sig=Signal.CardChangeForm(card)
                sig.preForm=preForm
                if isByEffect:
                    game.makeSignalReason(sig)
                signals.append(sig)

        for signal in signals:
            yield game.y_sendSignal(signal)
        return successNum


    def y_destroyCard(self,cardOrList: Union[Card, List[Card]])->int:
        if not cardOrList:
            return 0
        if type(cardOrList) != list:
            cardOrList = [cardOrList]

        game=self.game

        refugeList=[]
        effPeriod,effect=game.getDealingEffect()
        if effect:
            cardOrList=effect.removeNotAffectedInList(cardOrList)

            refugeList=yield self._y_dealBeforeRemovedSignal(cardOrList,"destroy")

        changePlaceSignals=[]
        signals=[]
        successNum=0
        dieList=[]
        paraID=game.genUniID()
        for card in cardOrList:
            if card in refugeList:
                self.duelNode.playanimFxOnRemovedCard(card.uniID,FX_ID.effectDestroy)
                continue

            if not card.canDestroy():
                if card.isOnField():
                    card.playanimFx(FX_ID.effectDestroy,ANIM.none,paraID=paraID)
                continue

            successNum+=1
            shouldDie=True
            anim=ANIM.animDie

            if effect and effect.hasFlagCount(EFF_FLAG.resistFromRemovedByEffect, card):
                effect.reduceFlagCount(EFF_FLAG.resistFromRemovedByEffect, card)
                anim=ANIM.getHit
                shouldDie=False

            card.playanimFx(FX_ID.effectDestroy,anim,paraID=paraID)
            if shouldDie:
                dieList.append(card)

        for card in dieList:
            if effPeriod!=EFF_PERIOD.costing and effect:
                if card.isOnField():
                    sig=Signal.DestroyedOnFieldByEffect(card)
                else:
                    sig=Signal.DestroyedByEffect(card)
            else:
                sig=Signal.Destroyed(card)
            game.makeSignalReason(sig)
            signals.append(sig)


            if card.isInHand():
                self.duelNode.playanimPlayerDiscard1Card(card.side, card)
            elif card.isInDeck():
                self.duelNode.playanimPlayerDeckRemove1Card(card.side,card)
            t=yield game._y_changeCardLocation(card, LOCATION.grave, card.side_0)
            changePlaceSignals.extend(t)


        for signal in changePlaceSignals:
            yield game.y_sendSignal(signal)

        for signal in signals:
            yield game.y_sendSignal(signal)

        return successNum

    def y_switch2MonstersController(self,card1:Card,card2:Card):
        game=self.game
        if not card1.isMonsterOnField():
            return False
        if not card2.isMonsterOnField():
            return False
        if card1.side==card2.side:
            return False

        effPeriod,effect=game.getDealingEffect()
        if effect:
            cardList=[card1,card2]
            cardList=effect.removeNotAffectedInList(cardList)
            if len(cardList)!=2:
                return False

            leave1=yield self._y_dealBeforeRemovedSignal([card1],"control")
            if leave1:
                if card2.entityID:
                    card2.playanimFx(FX_ID.teleportFx)
                self.duelNode.playanimFxOnRemovedCard(card1.uniID,FX_ID.teleportFx)
                return False

            leave2=yield self._y_dealBeforeRemovedSignal([card2],"control")
            if leave2:
                if card1.entityID:
                    card1.playanimFx(FX_ID.teleportFx)
                self.duelNode.playanimFxOnRemovedCard(card2.uniID,FX_ID.teleportFx)
                return False


        paraID=game.genUniID()
        changeLocationSigs=[]
        sigs=[]

        sig=Signal.MonsterChangeController()
        sig.card=card1
        self.game.makeSignalReason(sig)
        sigs.append(sig)

        sig=Signal.MonsterChangeController()
        sig.card=card2
        self.game.makeSignalReason(sig)
        sigs.append(sig)

        card2Side=card2.side
        card1Side=card1.side
        card1.playanimFx(FX_ID.teleportFx,ANIM.fallInGround,paraID)
        card2.playanimFx(FX_ID.teleportFx,ANIM.fallInGround,paraID)

        sigList=yield game._y_changeCardLocation(card1,LOCATION.monsterZone,card2Side,summonFx=FX_ID.teleportFx)
        changeLocationSigs.extend(sigList)
        sigList=yield game._y_changeCardLocation(card2,LOCATION.monsterZone,card1Side,summonFx=FX_ID.teleportFx)
        changeLocationSigs.extend(sigList)

        for sig in sigs:
            yield game.y_sendSignal(sig)

        for sig in changeLocationSigs:
            yield game.y_sendSignal(sig)

        return True



    def y_changeMonsterController(self,cardOrList:Union[Card, List[Card]],newside=0,effDuration:EFF_DURATION=EFF_DURATION.onceForever,uniqueSourceID=0,isByEffect=True):
        if not cardOrList:
            return 0
        if type(cardOrList) != list:
            cardOrList = [cardOrList]

        game=self.game

        refugeList=[]
        effect=None
        if isByEffect:
            effPeriod,effect=game.getDealingEffect()
            if effect:
                cardOrList=effect.removeNotAffectedInList(cardOrList)

                refugeList=yield self._y_dealBeforeRemovedSignal(cardOrList,"control")

        sigs=[]
        changeLocationSigs=[]
        changedList=[]
        successNum = 0
        for card in cardOrList:
            if card in refugeList:
                self.duelNode.playanimFxOnRemovedCard(card.uniID,FX_ID.teleportFx)
                continue

            if not card.isMonsterOnField():
                continue

            tempNewside=newside
            if tempNewside==0:
                tempNewside=card.getEnemySideTuple()[0]

            if game.freeMonsterSpace(tempNewside)==0:
                continue

            successNum+=1
            shoudChange=True
            anim=ANIM.fallInGround
            if isByEffect:
                if effect and effect.hasFlagCount(EFF_FLAG.resistFromRemovedByEffect, card):
                    effect.reduceFlagCount(EFF_FLAG.resistFromRemovedByEffect, card)
                    shoudChange=False
                    anim=ANIM.getHit

            if shoudChange:
                if effDuration!=EFF_DURATION.onceForever:
                    buff=CardBuff.controlled(effDuration,uniqueSourceID)
                    card._addBuff(buff)
                    card._recalBuffs()

            card.playanimFx(FX_ID.teleportFx,anim)

            if shoudChange:
                changedList.append((card,tempNewside))

        for card,tempNewside in changedList:
            sig=Signal.MonsterChangeController()
            sig.card=card
            if isByEffect:
                self.game.makeSignalReason(sig)
            sigs.append(sig)

            sigList=yield game._y_changeCardLocation(card,LOCATION.monsterZone,tempNewside,summonFx=FX_ID.teleportFx)
            changeLocationSigs.extend(sigList)


        for signal in changeLocationSigs:
            yield game.y_sendSignal(signal)

        for signal in sigs:
            yield game.y_sendSignal(signal)

        return successNum


    def y_banishCard(self, cardOrList: Union[Card, List[Card]]) -> int:
        if not cardOrList:
            return 0
        if type(cardOrList) != list:
            cardOrList = [cardOrList]

        game=self.game

        refugeList=[]
        effPeriod,effect=game.getDealingEffect()
        if effect:
            cardOrList=effect.removeNotAffectedInList(cardOrList)

            refugeList=yield self._y_dealBeforeRemovedSignal(cardOrList,"banish")


        changePlaceSigs=[]
        dieList=[]
        successNum=0
        paraID=game.genUniID()
        for card in cardOrList:
            if card in refugeList:
                self.duelNode.playanimFxOnRemovedCard(card.uniID,FX_ID.banish)
                continue


            if not card.canBanish():
                if card.isOnField():
                    card.playanimFx(FX_ID.banish,ANIM.none,paraID=paraID)
                continue
            successNum+=1

            shouldDie=True
            anim=ANIM.disappear
            if effect and effect.hasFlagCount(EFF_FLAG.resistFromRemovedByEffect, card):
                effect.reduceFlagCount(EFF_FLAG.resistFromRemovedByEffect, card)
                anim=ANIM.getHit
                shouldDie=False

            card.playanimFx(FX_ID.banish,anim,paraID=paraID)
            if shouldDie:
                dieList.append(card)

        for card in dieList:
            if card.isInHand():
                self.duelNode.playanimPlayerDiscard1Card(card.side, card)
            elif card.isInDeck():
                self.duelNode.playanimPlayerDeckRemove1Card(card.side,card)

            t=yield game._y_changeCardLocation(card, LOCATION.banish)
            changePlaceSigs.extend(t)


        for signal in changePlaceSigs:
            yield game.y_sendSignal(signal)

        return successNum

    def y_returnCardToHand(self, cardOrList: Union[Card, List[Card]], toWhoseSide=0)->int:
        if not cardOrList:
            return 0
        if type(cardOrList) != list:
            cardOrList = [cardOrList]

        game=self.game

        refugeList=[]
        effPeriod,effect=game.getDealingEffect()
        if effect:
            cardOrList=effect.removeNotAffectedInList(cardOrList)

            refugeList=yield self._y_dealBeforeRemovedSignal(cardOrList,"returnCardToHand")


        changePlaceSigs=[]
        paraID=game.genUniID()
        returnList=[]
        successNum=0
        for card in cardOrList:
            if card in refugeList:
                self.duelNode.playanimFxOnRemovedCard(card.uniID,FX_ID.returnToHand)
                continue

            if not toWhoseSide:
                tempSide=card.side_0
            else:
                tempSide=toWhoseSide

            if not card.canReturnToHand(tempSide):
                if card.isOnField():
                    card.playanimFx(FX_ID.returnToHand,ANIM.none,paraID=paraID)
                continue

            successNum+=1

            anim=ANIM.disappear
            shouldReturn=True

            if effect and effect.hasFlagCount(EFF_FLAG.resistFromRemovedByEffect, card):
                effect.reduceFlagCount(EFF_FLAG.resistFromRemovedByEffect, card)
                anim=ANIM.getHit
                shouldReturn=False

            card.playanimFx(FX_ID.returnToHand,anim,paraID=paraID)
            if shouldReturn:
                returnList.append((card,tempSide))

        for card,tempSide in returnList:
            self.duelNode.playanimPlayerAddCardToHand(tempSide, card)

            t=yield game._y_changeCardLocation(card, LOCATION.hand, tempSide)
            changePlaceSigs.extend(t)


        for signal in changePlaceSigs:
            yield game.y_sendSignal(signal)

        return successNum


    def y_returnCardToDeck(self, cardOrList: Union[Card, List[Card]], toWhoseSide=0, returnType:RETURN_TO_DECK=RETURN_TO_DECK.shuffle):
        if not cardOrList:
            return 0
        if type(cardOrList) != list:
            cardOrList = [cardOrList]

        game=self.game

        refugeList=[]
        effPeriod,effect=game.getDealingEffect()
        if effect:
            cardOrList=effect.removeNotAffectedInList(cardOrList)

            refugeList=yield self._y_dealBeforeRemovedSignal(cardOrList,"returnCardToDeck")


        returnList=[]
        changePlaceSigs=[]
        paraID=game.genUniID()
        successNum=0
        thecardAddedToDeck=[]
        for card in cardOrList:
            if card in refugeList:
                self.duelNode.playanimFxOnRemovedCard(card.uniID,FX_ID.returnToDeck)
                continue

            if toWhoseSide==0:
                tempSide=card.side_0
            else:
                tempSide=toWhoseSide



            if not card.canReturnToDeck(tempSide):
                if card.isOnField():
                    card.playanimFx(FX_ID.returnToDeck,ANIM.none,paraID=paraID)
                continue

            successNum+=1

            shouldReturn=True
            anime=ANIM.disappear
            if effect and effect.hasFlagCount(EFF_FLAG.resistFromRemovedByEffect, card):
                effect.reduceFlagCount(EFF_FLAG.resistFromRemovedByEffect, card)
                shouldReturn=False
                anime=ANIM.getHit

            card.playanimFx(FX_ID.returnToDeck,anime,paraID=paraID)
            if shouldReturn:
                returnList.append((card,tempSide))

        for card,tempSide in returnList:
            if card.isInHand():
                self.duelNode.playanimPlayerDiscard1Card(card.side, card)

            self.duelNode.playanimPlayerAddCardToDeck(card.side,card)

            t=yield game._y_changeCardLocation(card, LOCATION.deck, tempSide, returnToDeckType=returnType)
            changePlaceSigs.extend(t)


        for signal in changePlaceSigs:
            yield game.y_sendSignal(signal)
        return successNum



    def y_sendCardToGrave(self, cardOrList: Union[Card, List[Card]], toWhoseSide:int=0):
        if not cardOrList:
            return False
        if type(cardOrList) != list:
            cardOrList = [cardOrList]

        game=self.game

        refugeList=[]
        effPeriod,effect=game.getDealingEffect()
        if effect:
            cardOrList=effect.removeNotAffectedInList(cardOrList)
            refugeList=yield self._y_dealBeforeRemovedSignal(cardOrList,"sendCardToGrave")

        dieList=[]
        changePlaceSigs=[]
        successNum=0
        for card in cardOrList:
            if card in refugeList:
                continue

            if not toWhoseSide:
                tempside=card.side_0
            else:
                tempside=toWhoseSide

            if not card.canSendToGrave(tempside):
                continue

            successNum+=1

            shouldDIe=True
            anim=ANIM.disappear
            if effect and effect.hasFlagCount(EFF_FLAG.resistFromRemovedByEffect, card):
                effect.reduceFlagCount(EFF_FLAG.resistFromRemovedByEffect, card)
                anim=ANIM.getHit
                shouldDIe=False

            if card.isOnField():
                card.playanimFx(FX_ID.none,anim)

            if shouldDIe:
                dieList.append((card,tempside))

        for card,tempside in dieList:
            if card.isInHand():
                self.duelNode.playanimPlayerDiscard1Card(card.side, card,True)
            elif card.isInDeck():
                self.duelNode.playanimPlayerDeckRemove1Card(card.side,card,True)
            t=yield game._y_changeCardLocation(card, LOCATION.grave, tempside)
            changePlaceSigs.extend(t)

        for signal in changePlaceSigs:
            yield game.y_sendSignal(signal)
        return successNum


    def y_setCardToSpellZone(self, cardOrList: Union[Card, List[Card]], toWhoseSide=0)->int:
        if not cardOrList:
            return 0
        if type(cardOrList) != list:
            cardOrList = [cardOrList]
        game=self.game

        refugeList=[]
        effPeriod,effect=game.getDealingEffect()
        if effect:
            cardOrList=effect.removeNotAffectedInList(cardOrList)

            refugeList=yield self._y_dealBeforeRemovedSignal(cardOrList,"setCardToSpellZone")

        setList=[]
        changePlaceSigs=[]
        successNum=0
        for card in cardOrList:
            if card in refugeList:
                continue

            tempside=toWhoseSide
            if not toWhoseSide:
                tempside=card.side

            if not card.canSetToSpellZone(tempside):
                continue

            successNum+=1

            if effect and effect.hasFlagCount(EFF_FLAG.resistFromRemovedByEffect, card):
                effect.reduceFlagCount(EFF_FLAG.resistFromRemovedByEffect, card)
            else:
                setList.append((card,tempside))
                if card.isOnField():
                    card.playanimFx(FX_ID.none,ANIM.disappear)


        playedsides=[]
        for card,tempside in setList:
            #avatar anim
            if tempside not in playedsides:
                playedsides.append(tempside)

                if self.game.playerop==(tempside,OPERATE.setSpell):
                    anim=AVATAR_ANIM.setCardToFront
                    percent=random.random()
                    if percent<0.3:
                        anim=AVATAR_ANIM.setCardToFront
                    elif percent<0.6:
                        anim=AVATAR_ANIM.setCardToFront1
                    elif percent<0.9:
                        anim=AVATAR_ANIM.setCardToDisk
                    self.duelNode.playanimAvatarAnim(tempside,anim)

            if card.isInHand():
                self.duelNode.playanimPlayerDiscard1Card(card.side,CardData.getNone())
            if card.isInDeck():
                self.duelNode.playanimPlayerDeckRemove1Card(card.side,CardData.getNone(),True)
            t=yield game._y_changeCardLocation(card, LOCATION.spellTrapZone, tempside, FORM.set,ANIM.leaveListToField, summonFx=FX_ID.setCard)
            changePlaceSigs.extend(t)


        for signal in changePlaceSigs:
            yield game.y_sendSignal(signal)
        return successNum


    def y_moveCardToSpellZone(self, cardOrList: Union[Card, List[Card]], toWhoseSide=0, equipToMonster:Card=None,newCardType=CARD_TYPE.none):
        if not cardOrList:
            return 0
        if type(cardOrList) != list:
            cardOrList = [cardOrList]

        game=self.game

        refugeList=[]
        effPeriod,effect=game.getDealingEffect()
        if effect:
            cardOrList=effect.removeNotAffectedInList(cardOrList)

            refugeList=yield self._y_dealBeforeRemovedSignal(cardOrList,"moveCardToSpellZone")

        moveList=[]
        changePlaceSigs=[]
        equipSignals=[]
        successNum=0
        for card in cardOrList:
            if card in refugeList:
                continue

            tempSide=toWhoseSide
            if not toWhoseSide:
                tempSide=card.side

            if not card.canMoveToSpellZone(tempSide) and not equipToMonster:
                continue

            successNum+=1

            shouldMove=True
            anim=ANIM.disappear
            if effect and effect.hasFlagCount(EFF_FLAG.resistFromRemovedByEffect, card):
                effect.reduceFlagCount(EFF_FLAG.resistFromRemovedByEffect, card)
                if equipToMonster!=None:
                    successNum-=1
                shouldMove=False
                anim=ANIM.getHit

            if card.isOnField():
                card.playanimFx(FX_ID.none,anim)
            if shouldMove:
                moveList.append((card,tempSide))

        for card,tempSide in moveList:
            if card.isInHand():
                self.duelNode.playanimPlayerDiscard1Card(card.side,card,True)
            elif card.isInDeck():
                self.duelNode.playanimPlayerDeckRemove1Card(card.side,card,True)
            if newCardType:
                card.cardType=newCardType
            t=yield game._y_changeCardLocation(card, LOCATION.spellTrapZone, tempSide, FORM.face,ANIM.leaveListToField, summonFx=FX_ID.setCard)
            changePlaceSigs.extend(t)

            if equipToMonster!=None:
                #this is equip spell and need to equip to target
                isEquipSuccess = False
                if card.location == LOCATION.spellTrapZone and equipToMonster.isMonsterOnField():
                    if card not in equipToMonster.equipCardList:
                        equipToMonster.equipCardList.append(card)
                    card.equipToUID = equipToMonster.uniID
                    card.cardType=CARD_TYPE.equipSpell
                    sig = Signal.EquipTo(card)
                    sig.equipSpell = card
                    sig.monsterCard = card.getEquipToCard()
                    equipSignals.append(sig)
                    isEquipSuccess = True

                if not isEquipSuccess:
                    t=yield game._y_changeCardLocation(card,LOCATION.grave,tempSide)
                    changePlaceSigs.extend(t)

        for signal in changePlaceSigs:
            yield game.y_sendSignal(signal)
        for signal in equipSignals:
            yield game.y_sendSignal(signal)
        return successNum



    def y_damagePlayer(self, sideOrTuple:Union[int,Tuple], damageNum:int,fx=FX_ID.effectDamage):
        sideOrTuple=self._parseSide(sideOrTuple)
        signals=[]
        paraID=self.game.genUniID()
        for side in sideOrTuple:
            realNum=self.game.damagePlayer(side,damageNum,False)

            numberType=NUMBER_TYPE.damagePlayer
            if realNum<0:
                numberType=NUMBER_TYPE.heal

            self.duelNode.playanimFxToPlayer(side,fx,realNum,numberType,None,paraID)

            if realNum>=0:
                sig=Signal.PlayerLPLoseByEffect()
                sig.number=realNum
            else:
                sig=Signal.PlayerLPRecover()
                sig.number=-realNum
            sig.receiverPlayer=side
            self.game.makeSignalReason(sig)
            signals.append(sig)

        for sig in signals:
            yield self.game.y_sendSignal(sig)


    def y_healPlayer(self, sideOrTuple:Union[int,Tuple],healNum:int,fx=FX_ID.recoverHP):
        yield self.y_damagePlayer(sideOrTuple,-healNum,fx)

    def checkCanSpecialSummon(self,card:Card,toWhoseSide=0):
        game=self.game
        if toWhoseSide==0:
            toWhoseSide=card.side
        if game.freeMonsterSpace(toWhoseSide)==0:
            return False
        if not card.canSummon(card.side):
            return False
        return True


    def checkCanNormalSummon(self,card:Card, toWhoseSide=0, costNormalSummonChance=True, tributeNumChange:int=None)->bool:
        result=getBoolYieldReturn(self.y_normalSummon(True,card, toWhoseSide, costNormalSummonChance, tributeNumChange))
        return result


    """
    normal summon a card without tribute
    """
    def y_normalSummon(self, justCheck:bool, card:Card, toWhoseSide=0, costNormalSummonChance=True, tributeNumChange:int=None)->bool:
        game=self.game
        changePlaceSignals=[]

        callerSide=card.side

        if costNormalSummonChance:
            if game.normalSummonCntThisTurn[callerSide]>=game.normalSummonCntLimit[callerSide]:
                game.CANTUSE_LOG(makeStrNoTrans("OnlyXSummonPerTurn", game.normalSummonCntLimit[card.side]))
                return False


        if toWhoseSide==0:
            toWhoseSide=card.side


        if tributeNumChange!=None:
            tributeNum=tributeNumChange
        else:
            tributeNum = card.getNormalSummonTributeNum()

        if tributeNum<0:
            tributeNum=0

        cardGroups = []
        if tributeNum > 0:
            maxSearch = 10000
            if justCheck:
                maxSearch = 1
            basicFilter = Functor(fitter.canTribute, card)
            groupFitter = Functor(fitter.groupCanNormalSummonTribute, card)
            cardGroups: List[List[Card]] = self.searchCardGroup(LOCATION.monsterZone, toWhoseSide, CARD_TYPE.monster, 1, tributeNum,
                                                                None, basicFilter, groupFilter=groupFitter, maxSearchNum=maxSearch)
            if not len(cardGroups):
                game.CANTUSE_LOG("NotEnoughTributes")
                return False

        if game.freeMonsterSpace(toWhoseSide)==0 and tributeNum==0:
            return False


        normalSummonSig=Signal.NormalSummon(card)
        normalSummonSig.tributes=[]

        if not card.canSummon(card.side, normalSummonSig):
            return False


        if justCheck:
            return True


        if len(cardGroups):
            TEMP_MSG("found cardGroups ", cardGroups)
            selectedGroup=yield self.y_selectCardGroup(cardGroups,TITLE.tribute,callerSide,canCancel=True)
            if not selectedGroup:
                #player cancelled
                return False

            selectedGroup.sort(key=lambda seleCard: (seleCard.side == callerSide, seleCard.level))

            yield self.y_tributeCard(selectedGroup,toSummonCard=card)

            card.tributes=[]
            for tributeCard in selectedGroup:
                if 0:tributeCard:Card=tributeCard
                normalSummonSig.tributes.append(tributeCard)
                card.tributes.append(tributeCard)


        #avatar anim
        if self.game.playerop==(callerSide,OPERATE.normalSummon):
            self.duelNode.playanimAvatarAnim(callerSide,AVATAR_ANIM.summon)



        newform = card.getDefaultForm()
        card.resetReenterField()

        t=yield game._y_changeCardLocation(card, LOCATION.monsterZone, toWhoseSide, newform,ANIM.leaveListToField, summonFx=FX_ID.normalSummon)

        changePlaceSignals.extend(t)

        if card.isMonsterOnField():
            card.summonedTurn=self.game.curTurn

        if costNormalSummonChance:
            game.normalSummonCntThisTurn[callerSide]+=1

        DUEL_MSG("normal summon success ", card.getName())

        for signal in changePlaceSignals:
            yield game.y_sendSignal(signal)

        yield game.y_sendSignal(normalSummonSig)

        return True

    def checkCanExtraSummon(self, card:Card, needTribute:bool=False, costExtraChance=True,materialGroupFilter=None)->bool:
        result=getBoolYieldReturn(self.y_extraSummon(True, card, needTribute, costExtraChance,materialGroupFilter))
        return result

    """
    materialGroupFilter : function(cardList)->bool
    """
    def y_extraSummon(self, justCheck:bool, card:Card, needTribute:bool=False, costExtraChance=True,materialGroupFilter=None)->bool:
        game=self.game
        side=card.side

        if card.location != LOCATION.extraDeck:
            WARNING_MSG("Extra summon outside of the extra deck does not require tributes ",card.getName())
            needTribute=False

        if needTribute:
            if not game.checkLevelSumAndOrangeMonster(card.side, card.level):
                return False


        if costExtraChance:
            if game.extraSummonCntThisTurn[side]>=game.extraSummonCntLimit[side]:
                game.CANTUSE_LOG(makeStrNoTrans("OnlyXExtraSummonPerTurn", game.extraSummonCntLimit[card.side]))
                return False


        sig=Signal.ExtraSummon(card)
        sig.card=card
        sig.tributes=[]
        if not card.canSummon(card.side, sig):
            return False

        if not card.settedMaterialFilter:
            ERROR_MSG("sync monster not has settedMaterialFilter ",card.getName())
            return False


        cardGroups=[]
        if needTribute:
            basicFilter=Functor(fitter.canTribute,card)
            groupLimit=Functor(fitter.extraSummonLevelLimit, card.level)
            if justCheck:
                searchNum=1
            else:
                searchNum=10000
            cardGroups=self.searchCardGroup(card.materialLocationMask, side, CARD_TYPE.monster, card.materialMinNum, card.level, None, basicFilter, groupLimit, card.settedMaterialFilter, searchNum)

            if materialGroupFilter:
                for i in range(len(cardGroups)-1,-1,-1):
                    group=cardGroups[i]
                    if not materialGroupFilter(group):
                        del cardGroups[i]

            if not cardGroups:
                return False

        if justCheck:
            return True

        if cardGroups:
            tributeCards=yield self.y_selectCardGroup(cardGroups,TITLE.tribute,side,canCancel=True)
            if not tributeCards:
                return False

            for c in tributeCards:
                sig.tributes.append(c)

            shouldNum=len(tributeCards)
            successNum=yield self.y_tributeCard(tributeCards,toSummonCard=card)
            if successNum!=shouldNum:
                return False

        #avatar anim
        if self.game.playerop==(side,OPERATE.extraSummon):
            self.duelNode.playanimAvatarAnim(side,AVATAR_ANIM.summon)

        newform = card.getDefaultForm()

        yield self.y_specialSummon(card,side,newform,summonSignal=sig,fxID=FX_ID.bigfireSpecialSummon)

        if costExtraChance:
            game.extraSummonCntThisTurn[side]+=1

        return True

    def y_specialSummon(self, cardOrList: Union[Card, List[Card]], toWhoseSide=0, form: FORM = 0, buffIDOrList:Union[CARD_BUFF,List[CARD_BUFF]]=0, ignoreRequirement=False,summonSignal=None,fxID=FX_ID.specialSummon) -> int:
        if not cardOrList:
            return 0
        game=self.game
        if type(cardOrList) != list:
            cardOrList = [cardOrList]

        if len(cardOrList)>1 and summonSignal:
            ERROR_MSG("special summon multi cards with summonSignal")

        sigs=[]
        changePlaceSigs=[]

        successNum = 0
        successCardList=[]
        for card in cardOrList:
            tempside=toWhoseSide
            if not toWhoseSide:
                tempside=card.side

            if game.freeMonsterSpace(tempside)==0:
                continue

            if card.canSummon(tempside):
                if not summonSignal:
                    summonSignal = Signal.SpecialSummon(card)
                game.makeSignalReason(summonSignal)
                sigs.append(summonSignal)

                newForm=form
                if newForm not in (FORM.attack,FORM.defence,FORM.defenceSet):
                    newForm = card.getDefaultForm()

                card.resetReenterField()

                if not fxID:
                    fxID=FX_ID.specialSummon

                t=yield game._y_changeCardLocation(card, LOCATION.monsterZone, tempside, newForm, ANIM.leaveListToField,summonFx=fxID)
                changePlaceSigs.extend(t)

                if card.isMonsterOnField():
                    card.summonedTurn=self.game.curTurn

                if buffIDOrList:
                    if type(buffIDOrList)==int:
                        buffIDOrList=[buffIDOrList]
                    for buffID in buffIDOrList:
                        if buffID<CARD_BUFF._specialBuffStart:
                            ERROR_MSG("specialSummon addCardBuff error ",buffID)
                        else:
                            b=g_buffClasses[buffID](EFF_DURATION.onceForever)
                            card._addBuff(b)
                    card._recalBuffs()

                DUEL_MSG("special summon success ", card.getName())
                successCardList.append(card)
                successNum += 1

                #avatar anim
                callerSide=0
                effectperiod, effect = self.game.getDealingEffect()
                if effect and effect.owner:
                    callerSide=effect.owner.side
                else:
                    callerSide=card.side
                avatar=self.duel.avatars[callerSide]
                if time.time()-avatar.lastPlayAvatarAnim[0]>3:
                    self.duelNode.playanimAvatarAnim(callerSide,AVATAR_ANIM.summon)


        if len(successCardList)>1:
            sig=Signal.SpecialSummonMultiCards()
            sig.cardList=successCardList
            game.makeSignalReason(sig)
            sigs.append(sig)

        for signal in changePlaceSigs:
            yield game.y_sendSignal(signal)

        for signal in sigs:
            yield game.y_sendSignal(signal)

        return successNum



    def y_discoverCard(self,
                       side: int = 0,
                       poolName: str = None,
                       race=None,
                       attr=None,
                       cardType=None,
                       minLevel: int = None,
                       maxLevel: int = None,
                       count: int = 3,
                       title: str = None,
                       canCancel: bool = False) -> Card:
        """
        Hearthstone-style Discover: show count random cards from a pool, let the
        player pick one, add it to hand, and silently discard the rest.

        Source selection (mutually exclusive, poolName takes priority):
          poolName  — draw from a manually registered DiscoverPool named pool
          race/attr/cardType/minLevel/maxLevel — draw from the auto-filter pool

        Parameters
        ----------
        side        : player side; 0 = this effect's owner
        poolName    : name passed to DiscoverPool.getFromPool(); ignores filter args
        race        : RACE enum (e.g. RACE.DINOSAUR); None = no filter
        attr        : ATTR enum (e.g. ATTR.DARK); None = no filter
        cardType    : CARD_TYPE enum (monster/spell/trap/all); None = monsters only
        minLevel    : minimum level (inclusive); None = no limit
        maxLevel    : maximum level (inclusive); None = no limit
        count       : number of choices shown to the player (default 3)
        title       : selector title; defaults to TITLE.addToHand
        canCancel   : whether the player can skip the discover

        Returns
        -------
        The Card added to hand, or None if cancelled / pool empty.
        """
        from DiscoverPool import DiscoverPool

        if title is None:
            title = TITLE.addToHand

        # --- draw keys from the appropriate pool ---
        if poolName is not None:
            keys = DiscoverPool.instance().getFromPool(poolName, count)
        else:
            keys = DiscoverPool.instance().get(
                race=race, attr=attr, cardType=cardType,
                minLevel=minLevel, maxLevel=maxLevel, count=count,
            )

        if not keys:
            return None

        # --- create temporary cards at LOCATION.none ---
        tempCards = [self.game.createCard(k, self._parseSide(side)[0]) for k in keys]
        tempCards = [c for c in tempCards if c]   # filter out any createCard failures

        if not tempCards:
            return None

        # --- let the player choose ---
        picked = yield self.y_select1Card(tempCards, title, side, canCancel=canCancel)

        # --- move picked card to hand; clean up the rest ---
        for c in tempCards:
            if c is picked:
                yield self.y_returnCardToHand(c)
            else:
                # remove temp card from usedCards without triggering game events
                self.game.duel.usedCards.pop(c.uniID, None)

        return picked

    def y_winGameByEffect(self,winnerSide,reasonCard:Card):
        duel=self.duel

        for side in self.game.getEnemySideTuple(winnerSide):
            duel.setLoser(side,makeStrAllTrans(LOSE_REASON.cardEffect,"_CARD_KEY_"+reasonCard.cardKey))


    #send BeforeRemovedByEffect to cards,return leaved card list
    def _y_dealBeforeRemovedSignal(self,cardList,removeType:str):
        preLocations={}
        for card in cardList:
            preLocations[card.uniID]=card.location

        sig=Signal.BeforeRemovedByEffect()
        sig.cardList=list(cardList)
        sig.removeType=removeType
        self.game.makeSignalReason(sig)
        yield self.game.y_sendSignal(sig)

        refugeList=[]
        for card in cardList:
            if preLocations[card.uniID]& LOCATION.mask_onField!=0 and card.location&LOCATION.mask_onField==0:
                #already not on field
                refugeList.append(card)
        return refugeList


    def _________________________basicOperatesEnd(self):
        pass

    def onDestroy(self):
        self.game=None
        self.duelNode=None
        self.duel=None


