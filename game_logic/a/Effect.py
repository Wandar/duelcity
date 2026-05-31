# -*- coding: utf-8 -*-
from __future__ import annotations

from annos import *
from util import *
from a import Signal
from a.GameFunc import GameFunc
from UserType import CardData
from a.DuelConstants import *


OBSERVESIGNAL_QUICK_EFFECT=[Signal.BeforeActivateEffectOnField,Signal.InBattle]


class Effect(EffectData,GameFunc):
    owner:Card=None
    effUniID=0
    game:Game=None


    effType:EFF_TYPE=EFF_TYPE.active
    manaCost=0


    AI_HINT=[]
    EFF_POWER=0

    ####only useful if this is an activate effect
    specificOperate=OPERATE.activateEffect
    activateLocation=0
    ####

    observeSignals:Tuple[LOCATION, List[Signal.Signal]]=(0, [])

    isConnected=False
    # describe=""

    countLimit:COUNT_LIMIT=COUNT_LIMIT.oncePerTurn

    useCountThisTurn=0
    useCountThisDuel=0

    _savedTarget1:Union[Card, List[Card]]=None
    _savedTargetPlace1=None #if target changed location,
    _savedTarget2:Union[Card, List[Card]]=None
    _savedTargetPlace2=None #if target changed location,

    _triggerSignal=None

    # def setDescribe(self,s:str):
    # 	self.describe=s

    effectFlags=None  #{EFF_FLAG:{cardUniID:1}}


    #If card is sent to a new location not in enableLocation,the activation will be cancelled.This is auto generated.
    _enableLocation=0
    # observeSignals include LeaveXXX
    _OBSERVE_LEAVE_FIELD_SIGNAL=False

    def __init__(self,card:Card,order:int):
        EffectData.__init__(self,None)
        self.effectFlags={}
        self._savedTargetPlace1={}
        self._savedTargetPlace2={}
        self.originalCardKey=""
        self.originalOrder=0
        self.shortEff=""
        if getattr(self,"__IS_SHORT_EFFECT__",None):
            self.shortEff=self.__class__.__name__
        self.flag=0
        self.data=""
        self.order=order

        if card and card.game:

            ASSERT_MSG(card.cardKey_0,"init Effect cardKey_0==none")
            ASSERT_MSG(order!=0,"effect order==0")
            GameFunc.__init__(self,card.game,card.game.duel)

            if self.shortEff=="":
                self.originalCardKey=card.cardKey_0
                self.originalOrder=order
            self.owner:Card=card

            self.game=self.owner.game
            self.effUniID=self.game.genUniID()
            card.effects[order] = self

            if self.effType&EFF_TYPE.active:
                if self.activateLocation==0:
                    if self.owner.isSpell():
                        self.activateLocation= LOCATION.hand + LOCATION.spellTrapZone
                    elif self.owner.isTrap():
                        self.activateLocation=LOCATION.spellTrapZone
                    elif self.owner.isMonster():
                        self.activateLocation=LOCATION.monsterZone
            if self.effType==EFF_TYPE.active:
                self.observeSignals=(LOCATION.none, [])

            if len(self.observeSignals)<2 or type(self.observeSignals[0])!=int or type(self.observeSignals[1])!=list:
                ERROR_MSG("observeSignals format error:",card.getName())
                self.observeSignals=(LOCATION.none, [])

            for sig in self.observeSignals[1]:
                if sig.IS_LEAVE_SOMEWHERE:
                    self._OBSERVE_LEAVE_FIELD_SIGNAL=True
                    break

            if self._OBSERVE_LEAVE_FIELD_SIGNAL:
                self._enableLocation=LOCATION.mask_all
            else:
                if self.effType&EFF_TYPE.active:
                    self._enableLocation|=self.activateLocation
                if self.effType&EFF_TYPE.trigger or self.effType&EFF_TYPE.instant:
                    self._enableLocation|=self.observeSignals[0]


    def getClassName(self):
        return self.__class__.__name__

    def CANTUSE_LOG(self, s):
        self.game.CANTUSE_LOG(s)

    def initAsShortEffect(self,shortEffName):
        self.originalCardKey=""
        self.originalOrder=0
        self.shortEff=shortEffName

    def setManaCost(self,n:int):
        self.manaCost=n


    def setEffectAnim(self):
        pass


    def _getEffectUniName(self):
        return self.owner.getName()+"_"+self.originalCardKey+"_"+str(self.originalOrder)



    # def prepare(self):
    #     #count
    #     #mana
    #     self.game.manaMgr.reserveMana(self.getCamp(), self.manaCost)
    #     self.reserveCount+=1


    def onTurnStart(self):
        self.useCountThisTurn=0
        if self.countLimit!=COUNT_LIMIT.onlyOncePerDuel:
            if 0<self.order<=8:
                self.owner.flag &=~ (1<<(self.order-1))


    def checkCanActivate(self, signal,ignoreMana=False)->bool:
        returnValue=KBEngine.getCoroutineResult(self.y_costSuper(True, signal,0,ignoreMana))
        if returnValue==COROUTINE_HASYIELD_WHILECHECK:
            ERROR_MSG(self.__class__.__name__+"'s 'y_cost' method shouldn't contain yield function before 'justCheck return'")
            return False
        elif returnValue==COROUTINE_HASERROR:
            return False

        if not returnValue:
            return False


        returnValue=KBEngine.getCoroutineResult(self.y_activateSuper(True, signal))
        if returnValue==COROUTINE_HASYIELD_WHILECHECK:
            ERROR_MSG(self.__class__.__name__+"'s 'y_activate' method shouldn't contain yield function before 'justCheck return'")
            return False
        elif returnValue==COROUTINE_HASERROR:
            return False

        if not returnValue:
            return False

        return True


    def y_locationChange(self,oldSide,oldLocation,newSide,newLocation):
        pass


    def hasUseCount(self,selfeffuniName):
        if self.countLimit>=0:
            if self.useCountThisTurn==self.countLimit:
                return False
        elif self.countLimit==COUNT_LIMIT.sameNameOncePerTurn:
            if selfeffuniName in self.game.effectUseCntThisTurn:
                return False
        else:
            if self.countLimit==COUNT_LIMIT.onlyOncePerDuel:
                if self.useCountThisDuel!=0:
                    return False
        return True



    #card receive signal,called only if isConnected
    def y_signal(self,signal):
        pass

    def y_costSuper(self, justCheck:bool, signal,playEffectUniID=0,ignoreMana=False):
        if not justCheck:
            self._savedTargetPlace1.clear()
            self._savedTarget1=None
            self._savedTargetPlace2.clear()
            self._savedTarget2=None

        game=self.game
        if len(game.dealingEffectStack)>100:
            WARNING_MSG("activating effects > 100,maybe endless loop")
            return False


        isActivelyActivate=isSignal(signal,Signal.PlayerActivate)

        card=self.owner
        side=self.owner.side


        #card can't be activated on set turn
        if card.isSetInSpellZone() and card.beSetTurn==self.game.curTurn:
            return False


        if isActivelyActivate:
            #not active effect
            if self.effType&EFF_TYPE.active==0:
                return False

            if card.location& self.activateLocation==0:
                return False

            #activate effect can only used in my turn
            if side not in game.whoCanMove:
                return False

            #only main phase can activate active effect
            if self.effType&EFF_TYPE.trigger==0 and self.effType&EFF_TYPE.instant==0:
                if not game.isMainPhase():
                    game.CANTUSE_LOG("canOnlyActivateInMainPhase")
                    return False
        else:
            if card.location&self._enableLocation==0:
                return False


        #location free slot
        if card.isSpellTrapCard() and card.isInHand():
            if game.freeSpellSpace(side)==0:
                return False

        #manachange
        # if not ignoreMana:
        #     if not game.manaMgr.affordableEffect(self):
        #         if isActivelyActivate:self.CANTUSE_LOG("notAffordableMana")
        #         return False
        #
        #     #pay mana
        #     if not justCheck:
        #         self.game.manaMgr.payManaCostOfEffect(self)


        selfeffuniName=self._getEffectUniName()
        #count
        if not game.duel.INFINITE_USE_EFFECT:
            if not self.hasUseCount(selfeffuniName):
                if isActivelyActivate:self.CANTUSE_LOG("outOfCount")
                return False


        game.isCosting=True
        isSuccess=yield self.y_cost(justCheck,signal)
        game.isCosting=False


        if isSuccess==None or type(isSuccess) in (int,bool):
            isSuccess=bool(isSuccess)
        else:
            ERROR_MSG(f"{self.owner.getName()}'s effect y_cost not return bool,justCheck={justCheck}")
            isSuccess=True


        if not isSuccess:
            # if not justCheck: #manachange
            #     self.game.manaMgr.recoverManaCostOfEffect(self)
            return False

        if justCheck:
            return True

        if selfeffuniName not in self.game.effectUseCntThisTurn:
            self.game.effectUseCntThisTurn[selfeffuniName]=1
        else:
            self.game.effectUseCntThisTurn[selfeffuniName]+=1
        self.useCountThisTurn+=1
        self.useCountThisDuel+=1

        if not self.hasUseCount(selfeffuniName):
            if 0<self.order<=8:
                self.owner.flag|=1<<(self.order-1)


        #show a card in front of player
        targetCardOrList=[]
        if self._savedTarget1:
            if type(self._savedTarget1)==list:
                targetCardOrList.extend(self._savedTarget1)
            else:
                targetCardOrList.append(self._savedTarget1)
        if self._savedTarget2:
            if type(self._savedTarget2)==list:
                targetCardOrList.extend(self._savedTarget2)
            else:
                targetCardOrList.append(self._savedTarget2)

        for i in range(len(targetCardOrList)-1,-1,-1):
            targetCard=targetCardOrList[i]
            if not CardData.isSameType(targetCard):
                ERROR_MSG("target card is not legal")
                del targetCardOrList[i]


        sigs=[]
        if card.isSpellTrapCard():
            #if this is spell in hand,put it to the field
            if card.isInHand():
                changePlaceSigs=yield game._y_changeCardLocation(card, LOCATION.spellTrapZone, card.side, FORM.face, ANIM.leaveListToField,summonFx=FX_ID.useSpell)
                sigs.extend(changePlaceSigs)

            #if this is set card,flip it
            elif card.isSetInSpellZone():
                card.playSetSpellTrapUseEffect()


        game.waitingActivateEffects[playEffectUniID]=self
        #avatr anim
        percent=random.random()
        avatarAnim=AVATAR_ANIM.useCardEffect1
        if percent<0.3:
            avatarAnim=AVATAR_ANIM.useCardEffect1
        elif percent<0.6:
            avatarAnim=AVATAR_ANIM.useCardEffect2
        elif percent<0.9:
            avatarAnim=AVATAR_ANIM.useCardEffect3
        game.duelNode.playanimAvatarAnim(card.side,avatarAnim)

        #show shining card in front of the field
        game.duelNode.playanimShowEffectCard(card.side, playEffectUniID, card,self.getDescribe(), targetCardOrList,0)


        if self.owner.isOnField():
            signal=Signal.BeforeActivateEffectOnField()
        else:
            signal=Signal.BeforeActivateEffect()

        signal.card=self.owner
        signal.cardType=card.cardType
        signal.effect=self
        signal.isActively=isActivelyActivate
        sigs.append(signal)

        for signal in sigs:
            yield game.y_sendSignal(signal)

        if self.hasFlagCount(EFF_FLAG.activateCountered) or self.owner.isSilenced:
            game.duelNode.playanimShowedEffectCardBeCountered(playEffectUniID)


        #hide on field
        game.duelNode.playanimHideEffectCard(playEffectUniID,0.2)


        #TODO
        # if not justCheck and isSuccess and self.target!=None:
        #     if type(self.target)!=list:
        #         targetList=[self.target]
        #     else:
        #         targetList=self.target
        #     self.owner.playanimTargetTo(targetList)

        return True


    def y_cost(self,justCheck:bool,signal:Signal.Signal):
        return True


    def y_activateSuper(self,justCheck,signal,playEffectUniID=0):
        if justCheck:
            canActivate=yield self.y_activate(True,signal)
            if canActivate==None or type(canActivate) in (bool,int):
                canActivate=bool(canActivate)
            else:
                ERROR_MSG(f"{self.owner.getName()}'s y_activate not return bool while justCheck")
                canActivate=True
            return canActivate
        else:

            shouldActivate=True
            if self.hasFlagCount(EFF_FLAG.activateCountered) or self.owner.isSilenced:
                shouldActivate=False
                self.removeFlagCount(EFF_FLAG.activateCountered)
                cardEntity=self.owner.getCardEntity()
                if cardEntity:
                    cardEntity.playanimUseEffect("",True)

            if playEffectUniID not in self.game.waitingActivateEffects:
                ERROR_MSG("playEffectUniID not in self.game.showingEffectCards ",self.owner.getName())
            else:
                del self.game.waitingActivateEffects[playEffectUniID]


            isSuccess=False
            if shouldActivate:
                #if monster card,monster plays effect animation
                cardEntity = self.owner.getCardEntity()
                if cardEntity:
                    cardEntity.playanimUseEffect()
                isSuccess=yield self.y_activate(False,signal)
                if isSuccess==None or type(isSuccess) in (bool,int):
                    isSuccess=bool(isSuccess)
                else:
                    ERROR_MSG(f"{self.owner.getName()}'s y_activate not return bool while justCheck")
                    isSuccess=True

            #remove flag count
            self.removeFlagCountAll(EFF_FLAG.resistFromRemovedByEffect)
            return isSuccess

    def y_activate(self,justCheck:bool,signal:Signal.Signal):
        return True

    #card effect played end
    def y_activateEnd(self, playEffUniID):
        card = self.owner

        #spell trap card send to grave
        if card.isSpellTrapCard() and card.form==FORM.face and card.isInSpellZone():
            if not card.isContinuousOrEquipSpellTrap():
                yield self.game.y_sendCardToGrave(card)


    def isSignalQuickEffect(self,signal):
        if isSignal(signal,Signal.PlayerActivate):
            #can only activate in my turn
            if self.game.whoseTurn==self.getSide():
                return True
        elif isSignal(signal,Signal.BeforeActivateEffectOnField):
            #can only chain enemy's field effect
            if signal.effect.getSide()!=self.getSide():
                return True
        elif isSignal(signal,Signal.InBattle):
            #can only chain enemy's attack
            if signal.attackerCard.side!=self.getSide():
                return True
        return False



    def getDescribe(self):
        if not self.shortEff and self.originalOrder and self.originalCardKey:
            return makeCardEffectStr(self.originalCardKey,self.originalOrder)
        elif self.shortEff:
            return makeStrAllTrans("ShortEffectDescribe","ShortEffect:"+self.shortEff,"Describe:"+self.shortEff)
        else:
            ERROR_MSG("effect get Describe error ",self.owner.getName())
            return ""

    def getOnlyEffectDescribe(self):
        if not self.shortEff and self.originalOrder and self.originalCardKey:
            return makeCardEffectStr(self.originalCardKey,self.originalOrder)+"_ONLYEFF"
        elif self.shortEff:
            return makeStrAllTrans("ShortEffectDescribe","ShortEffect:"+self.shortEff,"Describe:"+self.shortEff)
        else:
            ERROR_MSG("effect get Describe error ",self.owner.getName())
            return ""


    def _____________fastFunc(self):
        pass

    def getDuel(self)->Duel:
        return self.game.duel

    def getSide(self)->int:
        return self.owner.side

    def checkAlly(self,card:Card):
        return card.side%2==self.owner.side%2

    def checkSideAlly(self,side:int):
        return side%2==self.owner.side%2

    #get all opposite's sides in tuple,such as (2,) if 1v1 game and (2,4) if 2v2 game
    def getEnemySideTuple(self)->Tuple[int]:
        return self.duel.getEnemySideTuple(self.owner.side)

    #get my side and ally side tuple
    def getAllySideTuple(self)->Tuple[int]:
        return self.duel.getAllySideTuple(self.owner.side)

    #for 2V2
    def filterEnemySide(self,selectFilter=None):
        opposideList=list(self.getEnemySideTuple())
        for i in range(len(opposideList)-1,-1,-1):
            if not selectFilter or selectFilter(opposideList[i]):
                pass
            else:
                del opposideList[i]
        return opposideList

    def y_select1EnemySide(self,opposideTuple=None):
        if opposideTuple:
           if len(opposideTuple)==1:
                return opposideTuple[0]
           else:
               selectList=list(opposideTuple)
        else:
            t=self.getEnemySideTuple()
            if len(t)==1:
                return t[0]
            selectList=list(t)

        optionList=[]
        for side in selectList:
            optionList.append(self.duel.avatars[side].c_nickName)

        option=yield self.duel.y_showPopup("title_select1Opposide","text_select1Opposide",self.getSide(),optionList,0)
        return optionList[option]

    def y_select1Side(self,sides):
        playerList=[]
        for side in sides:
            playerList.append(self.duel.avatars[side].c_nickName)

        option=yield self.duel.y_showPopup("title_select1side","text_select1side",self.getSide(),playerList,0)
        return sides[option]


    def getTriggerSignal(self):
        if not self._triggerSignal:
            ERROR_MSG("trigger Effect has no signal ",self.owner.getName())
            return None
        return self._triggerSignal


    def getPlayerAvatar(self)->AvatarCE:
        side=self.getSide()
        if not side:
            return None
        return self.game.duel.avatars[side]

    def removeNotAffectedInList(self, cardList:List[Card]):
        newList=[]
        for card in cardList:
            if not card.immunityMask:
                newList.append(card)
                continue

            if self.owner==card: #can always affect self
                newList.append(card)
                continue

            if self.owner.cardType&CARD_TYPE.spell!=0 and card.immunityMask&IMMUNITY_MASK.spell!=0:
                pass
            elif self.owner.cardType&CARD_TYPE.trap!=0 and card.immunityMask&IMMUNITY_MASK.trap!=0:
                pass
            elif self.owner.cardType&CARD_TYPE.monster!=0 and card.immunityMask&IMMUNITY_MASK.monsterEffect!=0:
                pass
            else:
                newList.append(card)
        return newList


    def addFlagCount(self,effFlag:EFF_FLAG,card:Card=None):
        if effFlag not in self.effectFlags:
            oneFlag=self.effectFlags[effFlag]={}
        else:
            oneFlag=self.effectFlags[effFlag]

        cardUniID=0
        if card:
            cardUniID=card.uniID
        if cardUniID not in oneFlag:
            oneFlag[cardUniID]=0
        oneFlag[cardUniID]+=1

    def removeFlagCountAll(self,effFlag:EFF_FLAG):
        if effFlag in self.effectFlags:
            del self.effectFlags[effFlag]

    def removeFlagCount(self,effFlag:EFF_FLAG,card:Card=None):
        cardUniID=0
        if card:
            cardUniID=card.uniID
        if effFlag in self.effectFlags:
            if cardUniID in self.effectFlags[effFlag]:
                self.effectFlags[effFlag][cardUniID]=0
        else:
            WARNING_MSG("effect removeFlagCount not found flag, cardKey=",self.owner.cardKey)

    def reduceFlagCount(self,effFlag:EFF_FLAG,card:Card=None):
        cardUniID=0
        if card:
            cardUniID=card.uniID
        if effFlag in self.effectFlags:
            t=self.effectFlags[effFlag]
            if cardUniID in t:
                t[cardUniID]-=1
                if t[cardUniID]<0:
                    WARNING_MSG("effect reduceFlagCount flag <0 cardKey=",self.owner.cardKey)
        else:
            WARNING_MSG("effect reduceFlagCount not found flag, cardKey=",self.owner.cardKey)


    def hasFlagCount(self,effFlag:EFF_FLAG,card:Card=None):
        cardUniID=0
        if card:
            cardUniID=card.uniID

        if effFlag in self.effectFlags:
            t=self.effectFlags[effFlag]
            if cardUniID in t and t[cardUniID]>0:
                return True
        return False

    def getShortEffectTailNumber(self):
        if not self.data:
            return None
        return int(self.data)

    #if you saved a list,getLegalTarget1 returns a list
    def saveTarget1(self, cardOrList:Union[Card, list]):
        self._savedTargetPlace1.clear()
        self._savedTarget1=None
        if cardOrList:
            if type(cardOrList) in (list,tuple):
                self._savedTarget1=list(cardOrList)
                for card in cardOrList:
                    self._savedTargetPlace1[card.uniID]=card.location
            else:
                self._savedTarget1=cardOrList
                self._savedTargetPlace1[cardOrList.uniID]=cardOrList.location

    def getLegalTarget1(self, checkLocationChange=True)->Union[Card, List[Card]]:
        if type(self._savedTarget1)==list:
            return self._getLegalTargetList1(checkLocationChange)
        savedTarget=self._savedTarget1
        if not savedTarget:
            return None

        if type(savedTarget)==list:
            if len(savedTarget)>=2:
                WARNING_MSG("getLegalTarget has multi targets")
                savedTarget=savedTarget[0]
            elif len(savedTarget)==1:
                savedTarget=savedTarget[0]
            else:
                return None

        #check location changed
        if checkLocationChange:
            if savedTarget.uniID not in self._savedTargetPlace1:
                return None
            if savedTarget.location!=self._savedTargetPlace1[savedTarget.uniID]:
                return None

        #check can affect
        return savedTarget

    def _getLegalTargetList1(self,checkLocationChange)->List[Card]:
        savedTargetList=self._savedTarget1
        if not savedTargetList:
            return []

        for i in range(len(savedTargetList)-1,-1,-1):
            card=savedTargetList[i]
            if card.uniID not in self._savedTargetPlace1:
                del savedTargetList[i]
            elif checkLocationChange:
                if card.location!=self._savedTargetPlace1[card.uniID]:
                    del savedTargetList[i]
        return savedTargetList


    def saveTarget2(self, cardOrList:Union[Card, list]):
        self._savedTargetPlace2.clear()
        self._savedTarget2=None
        if cardOrList:
            if type(cardOrList) in (list,tuple):
                self._savedTarget2=list(cardOrList)
                for card in cardOrList:
                    self._savedTargetPlace2[card.uniID]=card.location
            else:
                self._savedTarget2=cardOrList
                self._savedTargetPlace2[cardOrList.uniID]=cardOrList.location

    def getLegalTarget2(self,checkLocationChange=True)->Union[Card,List[Card]]:
        if type(self._savedTarget2)==list:
            return self._getLegalTargetList2(checkLocationChange)
        savedTarget=self._savedTarget2
        if not savedTarget:
            return None

        if type(savedTarget)==list:
            if len(savedTarget)>=2:
                WARNING_MSG("getLegalTarget has multi targets")
                savedTarget=savedTarget[0]
            elif len(savedTarget)==1:
                savedTarget=savedTarget[0]
            else:
                return None

        #check location changed
        if checkLocationChange:
            if savedTarget.uniID not in self._savedTargetPlace2:
                return None
            if savedTarget.location!=self._savedTargetPlace2[savedTarget.uniID]:
                return None

        #check can affect
        return savedTarget

    def _getLegalTargetList2(self,checkLocationChange)->List[Card]:
        savedTargetList=self._savedTarget2
        if not savedTargetList:
            return []

        for i in range(len(savedTargetList)-1,-1,-1):
            card=savedTargetList[i]
            if card.uniID not in self._savedTargetPlace2:
                del savedTargetList[i]
            elif checkLocationChange:
                if card.location!=self._savedTargetPlace2[card.uniID]:
                    del savedTargetList[i]
        return savedTargetList

    def freeMonsterSpace(self):
        return self.game.freeMonsterSpace(self.getSide())

    def freeSpellSpace(self):
        return self.game.freeSpellSpace(self.getSide())

    def freeExtraSummonChance(self):
        side=self.getSide()
        return self.game.extraSummonCntThisTurn[side]<self.game.extraSummonCntLimit[side]

    def freeNormalSummonChance(self):
        side=self.getSide()
        return self.game.normalSummonCntThisTurn[side]<self.game.normalSummonCntLimit[side]

    def getDeckLeftNum(self,side=0):
        side=self._parseSide(side)[0]
        return len(self.game.decks[side])


    def ________________simpleEffect(self):
        pass

    def y_discover1MonsterFromDeck(self):
        target=yield self.y_discover1CardFromDeck(CARD_TYPE.monster)
        return target

    def y_discover1SpellTrapFromDeck(self):
        target=yield self.y_discover1CardFromDeck(CARD_TYPE.mask_spellTrap)
        return target

    def y_discover1CardFromDeck(self,cardType:CARD_TYPE)->Card:
        cardInDeck=self.searchCards(LOCATION.deck,self.getSide(),cardType)
        if len(cardInDeck)==0:
            self.duel.avatars[self.getSide()].showPopup(True,"title_discover","title_notarget",["OK"],waitForAnim=True)
            return None
        if len(cardInDeck)>3:
            cardInDeck=random.sample(cardInDeck,3)
        thetarget=yield self.y_select1Card(cardInDeck,TITLE.addToHand)
        yield self.y_returnCardToHand(thetarget)
        return thetarget


    def ________________simpleEffectEnd(self):
        pass

    def ____________fastFuncEnd(self):
        pass

    def onDestroy(self):
        GameFunc.onDestroy(self)
