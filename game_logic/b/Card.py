from __future__ import annotations
from KBEngine import *

from a.CardBuff import *
from a.DuelConstants import *
from card_effects import shortEffects
from util import *
from UserType import CardData
from a.Effect import Effect, EquipSpellEffect
from a import Signal, fitter,CardBuff

if 0:from b.Game import Game






class Dice:
    amount = 1
    type: str = "D"
    suffix = 1

    def getRandom(self):
        finalNum = 0
        if self.type == "D":
            for i in range(self.amount):
                finalNum += random.randint(1, self.suffix)
        elif self.type == "C":
            for i in range(self.amount):
                finalNum += random.randint(0, 1) * self.suffix
        else:
            ERROR_MSG("illegal numType ", self.type)
        return finalNum


# class Attack:
#     string = ""
#     isNone = False
#     baseNum = 0
#     diceList: [Dice] = []
#
#     def __init__(self, string: str):
#         string = string.replace(" ", "")
#         self.string = string
#         if string == "":
#             self.isNone = True
#             self.baseNum = 0
#             self.diceList = []
#             return
#         """
#         such as: 2+3D2
#         """
#         self.baseNum = 0
#         self.diceList.clear()
#         arr = string.split('+')
#
#         try:
#             for s in arr:
#                 a = Dice()
#                 if s.isdigit():
#                     self.baseNum += int(s)
#                 elif "D" in s:
#                     arr2 = s.split("D")
#                     if arr2[0] == "":
#                         arr2[0] = "1"
#                     a.amount = int(arr2[0])
#                     a.type = "D"
#                     a.suffix = int(arr2[1])
#                 elif "C" in s:
#                     arr2 = s.split("C")
#                     if arr2[0] == "":
#                         arr2[0] = "1"
#                     a.amount = int(arr2[0])
#                     a.type = "C"
#                     if arr2[1] == "":
#                         arr2[1] = "1"
#                     a.suffix = int(arr2[1])
#                 else:
#                     raise
#                 if a.amount < 0 or a.suffix < 1:
#                     raise
#                 self.diceList.append(a)
#         except Exception as e:
#             ERROR_MSG("attack str error", self.string)
#             ERROR_MSG(e)
#             a = Dice()
#             a.amount = 1
#             a.type = "D"
#             a.suffix = 1
#             self.diceList = [a]
#
#     def getRandomNum(self):
#         finalNum = self.baseNum
#         for attackNum in self.diceList:
#             finalNum += attackNum.getRandom()
#         return finalNum
#
#     def _makeStr(self):
#         s = ""
#         if self.baseNum != 0:
#             s = str(self.baseNum)
#         for i in range(len(self.diceList)):
#             if s != "":
#                 s += "+"
#             attackNum = self.diceList[i]
#             if attackNum.type == "D":
#                 if attackNum.amount != 1:
#                     s += str(attackNum.amount)
#                 s += "D" + str(attackNum.suffix)
#             elif attackNum.type == "C":
#                 if attackNum.amount != 1:
#                     s += str(attackNum.amount)
#                 s += "C"
#                 if attackNum.suffix != 1:
#                     s += str(attackNum.suffix)
#
#         self.string = s


def parseAtkStr(s:str,isAtkOrRanged):
    if isAtkOrRanged:
        try:
            return int(s)
        except:
            return 0
    else:
        if s=="":
            return ATK.none
        try:
            return int(s)
        except:
            return ATK.none



class Card(CardData):
    # name = index = description = name_CN = ''
    # school = Effects = ''
    # numTargets = 0
    # aura = trigBoard = trigHand = trigDeck = deathrattle = trigEffect = None
    # options, overload = (), 0
    # info1 = info2 = None

    summonedTurn=0
    # equip spells auto-get the built-in EquipSpellEffect; set False to opt out and
    # supply a custom equip activation effect instead
    AUTO_EQUIP_EFFECT=True
    def __init__(self, cardKey="", game: Game = None, side=0):
        CardData.__init__(self, None)
        self.__dict__ = CardData.genDefaultAttr()
        if cardKey:
            if cardKey not in D_CARD:
                cardKey = ""
        else:
            cardKey = getattr(self, "CARD_KEY", "")
            if cardKey in D_CARD:
                cardKey = cardKey
            else:
                cardKey = ""
        if not cardKey:
            ERROR_MSG("createCard not found cardKey ", cardKey)
            cardKey = "ghoul"

        #==========================
        self.cardKey_0 = cardKey
        self.cardKey = 0  # card key in ALL_DATA.json

        self.uniID = 0  # unique id of 1 duel
        self.entityID = 0  # related client entity's id,only if this card is on the field

        self.side_0 = side  #original side
        self.side = 0  # 1 or 2,same as player's side,can be changed

        self.cardType_0: CARD_TYPE = CARD_TYPE.none
        self.cardType: CARD_TYPE = CARD_TYPE.none  #monster,spell,trap

        self.attr_0: ATTR = ATTR.none
        self.attr: ATTR = ATTR.none

        self.race_0: RACE = RACE.none
        self.race: RACE = RACE.none

        # self.costhint_0 = 0
        # self.costhint = 0
        self.preferRanged = False
        self.level_0 = 0
        self.level = 0

        self.atk_0:int = 0
        self.atk: int= 0
        self.rangeAtk_0 :int= 0
        self.rangeAtk: int = 0

        self.defence_0 = 0 #defence in ALL_DATA.json
        self.defence = 0

        self.shortEffectsStr_0: str = ""

        self.flag:CARD_FLAG=0

        self.tributes:List[CardData]=[]

        #===========================

        self.form: FORM = FORM.none  #melee or ranged or set
        self.state:CARD_STATE=CARD_STATE.normal
        self.turnStartForm: FORM = FORM.none
        self.preLocation: LOCATION = LOCATION.none  #preious location
        self.location: LOCATION = LOCATION.none  #in hand or in deck or on the field

        self.playerChangedFormCntThisTurn = 0
        self.cantChangeFormThisTurn=False

        self.color = 0
        self.acce = ""  #accessory

        self.series = None

        self._savedDataJson = {}

        self.attackCntThisTurn = 0
        self.attackCntLimitPerTurn = 0

        self.hasShown=False

        """
        Short Effects' keys : -1 -2 -3
        Effects' keys: 1 2 3
        0 is empty
        """
        self.effects: Dict[int, Effect] = {}
        self._modifiedEffectList: [Effect] = []  #this is setted only if this cards' effect is modified


        self.buffList:List[CardBuff]=[]
        self.buffIDList :List[CARD_BUFF]= []

        self.equipToUID=0
        self.equipCardList:List[Card]=[]

        self.immunityMask:IMMUNITY_MASK=0
        self.isSilenced=False

        self.beSetTurn = 0



        #=============
        self.materialLocationMask=0
        self.materialMinNum=0
        self.materialMaxNum=0
        self.settedMaterialFilter=None # function([Card]):
        self.materialCardFilter=None # function(Card):
        # NOTE: equipCardFilter is a method (see below); don't set an instance attr here
        # or it would shadow subclass overrides. Override the method to restrict targets.
        #==============

        self.game: Game = game
        self.attackCntLimitPerTurn = 1

        self.loadAttrFromDATA(cardKey)
        self.reinitAttr()


        self.shortEffectsInit()
        self.effectsInit()
        self._autoInitBuiltinEffects()

        if not self.settedMaterialFilter:
            if self.cardType&CARD_TYPE.whiteMonster==CARD_TYPE.whiteMonster:
                self.settedMaterialFilter=Functor(fitter.extraSummonFromExtraDeckFilter, self)
                self.materialMinNum=2
                self.materialLocationMask=LOCATION.monsterZone



    def loadAttrFromDATA(self, cardKey):
        self.cardKey = self.cardKey_0 = cardKey
        D = D_CARD[self.cardKey]

        cardType = cardTypeStrToInt(D["type"],cardKey)
        self.cardType_0 = cardType

        if self.cardType_0 & CARD_TYPE.monster > 0:
            self.attr_0 = cardAttrStrToInt(D["attr"],cardKey)
            self.race_0 = cardRaceStrToInt(D["race"],cardKey)
            self.level_0 = D["level"]
            # self.costhint_0 = D["costhint"]
            self.atk_0 = parseAtkStr(D['atk'],True)
            self.rangeAtk_0 =parseAtkStr(D['range'],False)
            self.defence_0 = parseAtkStr(D['def'],True)
            if 'preferRanged' in D["extradata"] and D["extradata"]["preferRanged"]:
                self.preferRanged = True
        elif self.cardType_0 & (CARD_TYPE.spell | CARD_TYPE.trap) != 0:
            self.attr_0 = ATTR.none
            self.race_0 = RACE.none
            self.level_0 = 0
            # self.costhint_0 = D["costhint"]
            self.atk_0 = 0
            self.rangeAtk_0 = 0
            self.defence_0=0

        self.shortEffectsStr_0 = D['short_effects']
        self.series = D['series'].split(",")

    def reinitAttr(self):
        self._reinitBuffAttr()
        self.cardKey = self.cardKey_0
        self.side=self.side_0
        self.cardType = self.cardType_0
        # self.costhint = self.costhint_0
        self.defence = self.defence_0


    def _reinitBuffAttr(self):
        self.isSilenced=False
        self.immunityMask=0
        self.attackCntLimitPerTurn=1
        self.attr = self.attr_0
        self.race = self.race_0
        self.level = self.level_0
        self.atk=self.atk_0
        self.rangeAtk=self.rangeAtk_0
        self.defence=self.defence_0


    def CANTUSE_LOG(self, s):
        self.game.CANTUSE_LOG(s)


    def shortEffectsInit(self):
        arr = self.shortEffectsStr_0.split(',')
        order = 0
        for s in arr:
            s = s.strip()
            if s == "":
                continue

            hasNum = False
            hasData = False
            num = 0
            data = ""
            if ":" in s:
                temparr = s.split(":")
                if len(temparr) != 2:
                    ERROR_MSG("short effect parse error ", s, self.getName())
                    continue
                shortEffstr = temparr[0]
                data = temparr[1]
                hasData = True
            else:
                hasNum, shortEffstr, num = split_string_with_number_suffix(s)

            shortEffstr = shortEffstr.strip()
            if shortEffstr not in g_shortEffects:
                ERROR_MSG("%s not recognize shortEffect %s" % (self.getName(), shortEffstr))
                continue
            ShortEffClass = g_shortEffects[shortEffstr]
            shortEffNeedNum = getattr(ShortEffClass, "NEED_NUM", False)
            if shortEffNeedNum and not hasNum:
                ERROR_MSG(f"{self.getName()} shortEffect {shortEffstr} need a number")
                hasNum = True
                num = 1
            elif not shortEffNeedNum and hasNum:
                ERROR_MSG(f"{self.getName()} shortEffect {shortEffstr} doesnt need a number")
                hasNum = False
                num = 0

            order -= 1
            e = ShortEffClass(self, order)
            self.effects[order] = e
            e.shortEff = shortEffstr
            if hasNum:
                e.data = str(num)
                e.number_0 = num
            if hasData:
                e.data = data

    def effectsInit(self):
        #init effect
        pass

    def _autoInitBuiltinEffects(self):
        """Attach type-driven built-in effects that every such card shares, so authors
        don't wire them by hand. Currently: the equip-spell activation effect."""
        if self.AUTO_EQUIP_EFFECT and self.cardType_0 & CARD_TYPE.equipSpell == CARD_TYPE.equipSpell:
            if self.getEffect(EquipSpellEffect) is None:
                self.initEffect(EquipSpellEffect)

    def initEffect(self, EffectClass):
        if len(self.effects):
            order = max(max(self.effects.keys()), 0) + 1
        else:
            order = 1
        self.effects[order] = EffectClass(self, order)

    #TODO add remove
    def _addEffect(self,EffectClass):
        pass

    def _removeEffect(self,EffectClass):
        pass

    def initMaterialFilter(self, materialFilter, minNum=0, maxNum=0, locationMask=LOCATION.none, cardFilter=None):
        if minNum==0:
            ERROR_MSG("initMaterialFilter minNum ==0 :",self.getName())
            return

        self.settedMaterialFilter=materialFilter
        self.materialMinNum=minNum
        if maxNum==0:
            maxNum=minNum
        elif maxNum<0:
            maxNum=999999
        self.materialMaxNum=maxNum
        if locationMask==LOCATION.none:
            if self.cardType&CARD_TYPE.fusionMonster==CARD_TYPE.fusionMonster:
                locationMask=LOCATION.hand+LOCATION.monsterZone
            elif self.cardType&CARD_TYPE.whiteMonster==CARD_TYPE.whiteMonster:
                locationMask=LOCATION.monsterZone
        self.materialLocationMask=locationMask
        self.materialCardFilter=cardFilter

    def materialFilter(self,cards:List[Card]):
        pass

    def equipCardFilter(self,card):
        return True


    def getEffect(self, effectClsOrName) -> Effect:
        if type(effectClsOrName)!=str:
            effectClsOrName=effectClsOrName.__name__
        for order, effect in self.effects.items():
            if effect.__class__.__name__ == effectClsOrName:
                return effect
        return None


    #return effect order,if not found return 0
    def checkHasEffect(self,effect:Effect)->int:
        for order,eff in self.effects.items():
            if eff==effect:
                return order
        return 0

    def getCurLocationActivateEffectList(self):
        l=[]
        for order,eff in self.effects.items():
            if eff.effType& EFF_TYPE.active and eff.activateLocation &self.location:
                l.append(eff)
        return l


    def getNormalSummonTributeNum(self):
        num = 0
        if 4 < self.level <= 6:
            num = 1
        elif self.level > 6:
            num = 2
        return num

    """
    
    """


    def setDirty(self):
        self.game.duel.dirtyCards[self.uniID] = self

    def getDuel(self) -> "Duel":
        return self.game.duel

    def getBasicCardType(self):
        if self.cardType&CARD_TYPE.monster:
            return CARD_TYPE.monster
        if self.cardType&CARD_TYPE.spell:
            return CARD_TYPE.spell
        if self.cardType&CARD_TYPE.trap:
            return CARD_TYPE.trap
        ERROR_MSG("getBasicCardType None ",self.cardKey)
        return CARD_TYPE.spell

    def getName(self):
        n = D_CARD[self.cardKey]["name_en"]
        if not n:
            n = D_CARD[self.cardKey]["key"]
        return n

    def getCardEntity(self) -> CardEntityCE:
        if self.entityID == 0:
            return None
        if self.entityID not in entities:
            ERROR_MSG("cardEntityID not in entities", self.entityID)
            return None
        return entities[self.entityID]

    def ______________________spell(self):
        pass

    def ___________________can(self):
        pass



    def canBeDamage(self):
        if self.location& LOCATION.mask_onField:
            return True
        return False

    def canChangeController(self, newSide):
        if self.location==0:
            return False
        if not self.isMonsterOnField():
            return False
        return True

    def canChangeForm(self,newForm):
        if not self.entityID:
            ERROR_MSG("card ChangeForm no entityID")
            return False
        return True

    def canDestroy(self):
        if self.location==0:
            return False
        if self.location & (LOCATION.banish + LOCATION.grave):
            return False

        return True

    def canBanish(self):
        if self.location==0:
            return False
        if self.location == LOCATION.banish:
            return False
        return True

    def canTribute(self, reasonCard=None):
        if self.location==0:
            return False
        if self.location & (LOCATION.grave + LOCATION.banish):
            return False
        return True

    def canReturnToHand(self, newside):
        if self.location==0:
            return False
        if self.side == newside and self.location == LOCATION.hand:
            return False
        return True

    def canReturnToDeck(self, newside):
        if self.location==0:
            return False
        if self.side == newside and self.location == LOCATION.deck:
            return False
        return True

    def canSendToGrave(self,newside):
        if self.location == LOCATION.grave and self.side==newside:
            return False
        return True

    def canSetToSpellZone(self, side=0):
        if not side:
            side = self.side

        if self.location==0:
            return False

        if side == self.side and self.location & LOCATION.spellTrapZone > 0 and self.form==FORM.set:
            #alreay set in SpellZone
            return False

        if self.game.freeSpellSpace(side)==0:
            return False

        return True

    def canMoveToSpellZone(self, side=0):
        if not side:
            side = self.side

        if self.location==0:
            return False

        if side == self.side and self.location & LOCATION.spellTrapZone > 0 :
            #alreay in spell zone
            return False

        if self.game.freeSpellSpace(side)==0:
            return False

        return True

    def canEquipToMonster(self, monster):
        if self.location==0:
            return False
        if not monster.isMonsterOnField():
            return False
        return True

    """
    if this monster can be treated as 2 tributes,return 2
    normally return 1
    if this monster cant be treated as tribute,return 0
    """
    #return 1 or 0
    def getTributePoint(self, summonType: SUMMON_TYPE, reasonCard):
        if not self.canTribute(reasonCard):
            return 0

        if summonType == SUMMON_TYPE.normalSummon:
            return 1
        if summonType == SUMMON_TYPE.extraSummon:
            return self.level


    def canSummon(self, side, signal=None):
        if not self.cardType_0&CARD_TYPE.monster:
            return False
        if self.isInMonsterZone():
            return False

        if isSignal(signal, Signal.NormalSummon):
            if not self.checkBuffCanNormalSummon():
                return False
        elif isSignal(signal, Signal.ExtraSummon):
            if not self.checkBuffCanExtraSummon():
                return False
        else:
            if not self.checkBuffCanSpecialSummon():
                return False
        return True

    def canNormalSummon(self):
        if not self.checkBuffCanNormalSummon():
            return False
        return True

    def canSpecialSummon(self,signal=None):
        return True

    def canExtraSummon(self):
        return True


    def _________________endCan(self):
        pass

    def __________________callback(self):
        pass

    def onTurnStart(self):
        self.turnStartForm = self.form

        self.resetReenterField()

        for effectID, effect in self.effects.items():
            effect.onTurnStart()

    def _________________basicChecker(self):
        pass

    def checkBuffCanNormalSummon(self):
        return True

    def checkBuffCanSpecialSummon(self):
        return True

    def checkBuffCanExtraSummon(self):
        return True

    def checkBuffCanPlayerChangeForm(self):
        return True

    def checkBuffNeedTributes(self):
        return True

    def checkBuffCanAttack(self):
        return True

    def checkBuffCanTribute(self):
        return True

    def checkBuffCanTakeDamage(self):
        return True

    def checkBuffCanBeAffectedByEffect(self):
        return True

    def _________________basicCheckerEnd(self):
        pass

    def ____________________basicOperates(self):
        pass


    def isMonster(self):
        return self.cardType & CARD_TYPE.monster > 0

    def isOrangeNamedMonster(self):
        return self.cardType & CARD_TYPE.orangeMonster==CARD_TYPE.orangeMonster

    def isMonsterOnField(self):
        return self.isMonster() & self.isOnField()

    def isWhiteMonster(self):
        return self.cardType & CARD_TYPE.monster and self.cardType & CARD_TYPE.whiteMonster

    def isSpell(self):
        return self.cardType & CARD_TYPE.spell > 0

    def isTrap(self):
        return self.cardType & CARD_TYPE.trap > 0

    def isSpellTrapCard(self):
        return self.cardType & (CARD_TYPE.spell | CARD_TYPE.trap) > 0

    def isContinuousOrEquipSpellTrap(self):
        return self.cardType in (CARD_TYPE.continuousSpell,CARD_TYPE.continuousTrap,CARD_TYPE.equipSpell)

    def isOnField(self):
        return self.location & LOCATION.mask_onField > 0

    def isInHand(self):
        return self.location & LOCATION.hand > 0

    def isInDeck(self):
        return self.location & LOCATION.mask_inDecks > 0

    def isInMonsterZone(self):
        return self.location & LOCATION.monsterZone > 0

    def isInSpellZone(self):
        return self.location & LOCATION.spellTrapZone > 0

    def isSetInSpellZone(self):
        return self.form == FORM.set and self.location & LOCATION.spellTrapZone > 0

    def _equipToCard(self,thecard:Card):
        self.equipToUID=thecard.uniID
        if self not in thecard.equipCardList:
            thecard.equipCardList.append(self)

    def getEquipedCardList(self):
        pass

    def getEquipToCard(self):
        if not self.equipToUID:
            return None
        return self.getDuel().usedCards[self.equipToUID]

    def y_cardChangeLocation(self, preLocation,preSide):
        isChangedLocation=False
        if preLocation!=self.location:
            isChangedLocation=True

        if preLocation != LOCATION.spellTrapZone and self.location == LOCATION.spellTrapZone and self.form & FORM.set:
            self.beSetTurn = self.game.curTurn
        else:
            self.beSetTurn=0

        #effects
        for effect in tuple(self.effects.values()):
            observeLocation=effect.observeSignals[0]

            if observeLocation!=0:
                if observeLocation & self.location != 0:
                    self.game.effectConnect(effect)
                else:
                    if effect._OBSERVE_LEAVE_FIELD_SIGNAL:
                        self.game._leaveLocationEffectList.append(effect)
                    else:
                        self.game.effectDisconnect(effect)
            yield effect.y_locationChange(preSide,preLocation, self.side,self.location)



    def getCurNumber(self)->float:
        if self.isDefence():
            return self.defence
        return self.atk


    def canBattle(self,isAttacker):
        if not self.isMonster():
            return False
        if not self.isInMonsterZone():
            return False
        if not self.getCardEntity():
            ERROR_MSG("card on monsterField but no cardEntity")
            return False
        if isAttacker and self.form!=FORM.attack:
            return False

        return True

    def getDefaultForm(self):
        if self.isMonster():
            return FORM.attack
        else:
            return FORM.face

    def resetReenterField(self):
        self.attackCntThisTurn = 0
        self.playerChangedFormCntThisTurn = 0
        self.cantChangeFormThisTurn=False

    def ____________________basicOperatesEnd(self):
        pass

    def ____________________buff(self):
        pass

    def setData(self, key, d):
        self._savedDataJson[key] = str(d)

    def getData(self, key)->str:
        if key not in self._savedDataJson:
            return None
        return self._savedDataJson[key]

    def delData(self, key):
        if key in self._savedDataJson:
            del self._savedDataJson[key]

    #if add a new buff return true,if already has,return false
    def _addBuff(self,buff:CardBuff):
        #use TYPE to solve conflict,such as "+1 atk" and "atk becomes 1"
        if buff.TYPE:
            if buff.duration==EFF_DURATION.onceForever:
                #if has any IS_CHANGE_TO&fromSource buff,dont add
                for t in self.buffList:
                    if t.TYPE==buff.TYPE and t.IS_CHANGE_TO and t.duration==EFF_DURATION.fromSource:
                        return False

            if buff.IS_CHANGE_TO:
                #del all onceForever
                for i in range(len(self.buffList)-1,-1,-1):
                    t=self.buffList[i]
                    if t.TYPE==buff.TYPE and t.duration==EFF_DURATION.onceForever:
                        del self.buffList[i]

        isNewBuff=True
        if buff.uniqueSourceID:
            #delete same uniqueSourceID
            for i in range(len(self.buffList)-1,-1,-1):
                t:CardBuff=self.buffList[i]
                if t.BUFF_ID==buff.BUFF_ID and t.uniqueSourceID==buff.uniqueSourceID:
                    buff.addTurn=self.buffList[i].addTurn
                    del self.buffList[i]
                    isNewBuff=False

        buff.owner=self
        if buff.addTurn==0:
            buff.addTurn=self.game.curTurn
        self.buffList.append(buff)
        self.game._buffedCards[self.uniID]=self

        return isNewBuff


    def _removeBuff(self,buff:CardBuff):
        if buff in self.buffList:
            self.buffList.remove(buff)

    #return removed buffs
    def _removeBuffBySource(self,sourceID)->List[CardBuff]:
        if not sourceID:
            ERROR_MSG("_removeBuffBySource uniqueSourceID==0")
            return []
        removed=[]
        for i in range(len(self.buffList)-1,-1,-1):
            buff:CardBuff=self.buffList[i]
            if buff.uniqueSourceID==sourceID:
                removed.append(self.buffList[i])
                del self.buffList[i]
        return removed

    def removeBuffByID(self,buffID:CARD_BUFF):
        for i in range(len(self.buffList)-1,-1,-1):
            buff:CardBuff=self.buffList[i]
            if buff.uniqueSourceID!=0:
                if buff.BUFF_ID==buffID:
                    del self.buffList[i]
        self._recalBuffs()


    def _removeAllBuffs(self):
        self.buffList.clear()

    def _recalBuffs(self):
        self._reinitBuffAttr()

        fromSourceList=[]
        for buff in self.buffList:
            if buff.duration==EFF_DURATION.fromSource:
                fromSourceList.append(buff)
            else:
                buff.onBuff(self)
        for buff in fromSourceList:
            buff.onBuff(self)

        self._mergeListToBuffs()
        self._reconcileGrantedShortEffects()

    def _reconcileGrantedShortEffects(self):
        """
        Keep runtime-granted short effects in sync with the ShortEffectBuffs currently
        on this card: create+connect newly granted ones, disconnect+remove those whose
        grant buff is gone. Static short effects (from card data) carry
        _isGrantedShortEffect==False and are never touched here.

        Runs inside _recalBuffs, so it rides every buff change/removal path
        (turn-end sweep, battle-end sweep, remove-by-source, remove-by-id).
        """
        # short effect names still wanted by a grant buff -> the buff that wants it
        desired = {}
        for buff in self.buffList:
            if buff.BUFF_ID == CARD_BUFF.shortEffectAdd:
                if 0:buff:ShortEffectBuff=buff
                desired[buff.shortEffectName] = buff

        # names already realized as ANY effect (static or granted) + granted orders
        presentNames = set()
        grantedOrders = []
        for order, eff in self.effects.items():
            presentNames.add(eff.__class__.__name__)
            if eff._isGrantedShortEffect:
                grantedOrders.append(order)

        if not desired and not grantedOrders:
            return

        # drop granted effects no longer wanted by any buff
        for order in grantedOrders:
            eff = self.effects[order]
            if eff.__class__.__name__ not in desired:
                self.game.effectDisconnect(eff)
                del self.effects[order]

        # create effects newly wanted that aren't realized yet (static one wins if present)
        for name, buff in desired.items():
            if name in presentNames:
                continue
            if name not in g_shortEffects:
                ERROR_MSG("_reconcileGrantedShortEffects unknown shortEffect ", name, self.getName())
                continue
            ShortEffClass = g_shortEffects[name]
            order = min(min(self.effects.keys(), default=0), 0) - 1
            eff = ShortEffClass(self, order)   # Effect.__init__ registers it into self.effects
            eff.shortEff = name
            eff._isGrantedShortEffect = True
            eff.data = buff.data
            observeLocation = eff.observeSignals[0]
            if observeLocation != 0 and observeLocation & self.location != 0:
                self.game.effectConnect(eff)

    def recalBuffsAndOnDataChanged(self,fx=FX_ID.none,paraID=0):
        self._recalBuffs()
        self.onDataChangedFx(fx,paraID)


    def _mergeListToBuffs(self):
        self.buffIDList.clear()
        for buff in self.buffList:
            if buff.BUFF_ID not in self.buffIDList:
                self.buffIDList.append(buff.BUFF_ID)


    def hasBuff(self,buffID:CARD_BUFF):
        return buffID in self.buffIDList


    def getEnemySideTuple(self)->Tuple[int]:
        return self.game.getEnemySideTuple(self.side)

    #get my side and ally side tuple
    def getAllySideTuple(self)->Tuple[int]:
        return self.game.getAllySideTuple(self.side)

    def isSameName(self,cardKey):
        if self.cardKey==cardKey:
            return True
        return False


    def _____________________buffEnd(self):
        pass

    def getSummonFromExtraOperates(self):
        return []

    def canDirectAttack(self):
        pass

    def canUseActiveEffect(self):
        pass

    def resetColor(self):
        pass


    def isFaceUp(self):
        if self.form & FORM.set == 0:
            return True
        return False

    def _________________________________End(self):
        pass

    def ______________effects(self):
        pass



    def playSetSpellTrapUseEffect(self):
        if self.entityID==0:
            ERROR_MSG("playanimSetCardUseEffect no entityID")
            return
        if self.form!=FORM.set:
            ERROR_MSG("playSetCardUseEffect not set")
            return
        self.setShowed()
        self.form=FORM.face
        cardEntity=self.getCardEntity()
        cardEntity.c_cardData=self
        cardEntity.playanimSetCardUseEffect(self)
    """
    play fx,then play anim
    
    """

    def playanimFx(self, fx: FX_ID, anim: ANIM = 0, number: int = 0, numberType=NUMBER_TYPE.dontshow, fromCard=None,fx2:FX_ID=0,
                   paraID=0):
        self.setShowed()
        if not fromCard:
            fromCard = CardData.getNone()
        en = self.getCardEntity()
        if en:
            en.c_cardData=self
            en.mc_playanimFx(fx, anim, number, numberType, fromCard, fx2,paraID)
            if ANIM.dieAnimStart__ < anim < ANIM.dieAnimEnd__:
                en.isPlayingLeavingAnim = True
        else:
            self.game.duelNode.mc_playanimCardFx(self, fx, anim, number, numberType, fromCard,paraID)


    """
    call this after changed data such as attr,race,level
    
    if this card is in hand or in deck,the animation can only be seen by owner
    
    fx: Flash Effect
    anim: the monster's animation
    """
    def onDataChangedFx(self, fx=FX_ID.none, anim=ANIM.none, fromCard=None, paraID=0):
        if self.location & (LOCATION.banish|LOCATION.grave|LOCATION.mask_onField):
            #if this card is in banish or grave or on field,play changeData fx
            en=self.getCardEntity()
            if en:
                en.c_cardData=self
            self.playanimFx(fx,anim,fromCard=fromCard,paraID=paraID)
        elif self.location& LOCATION.mask_notOnField:
            #if this card is in deck or hand,update the list
            self.game.modifyCardList(self.side, self.location, 0, self, anim)


    def changeCard(self,newKey):
        if self.hasShown:
            ERROR_MSG("jcakjsbcjc")
            return
        if self.entityID:
            ERROR_MSG("jbajshkcbvahjc")
            return
        if self.equipCardList:
            ERROR_MSG("kjabcshjc")
            return

        self.loadAttrFromDATA(newKey)
        self.reinitAttr()
        self.effects.clear()
        self._modifiedEffectList.clear()
        self.shortEffectsInit()
        self.effectsInit()
        self._autoInitBuiltinEffects()
        self._recalBuffs()

    def _transformInPlace(self, newKey):
        """
        Swap this card's identity to newKey IN PLACE (no summon / no new entity).
        uniID, location, side (controller), equipCardList and buffList are preserved;
        only the printed identity (cardKey/type/base stats) and the effect set change.

        Safe for on-field cards: old effects are detached from the signal bus before the
        swap and the new card's effects are connected for the current location afterwards,
        so no stale observers are left in the signal lists.
        """
        game = self.game

        # 1. tear the old effects off the signal bus (effectDisconnect is a no-op if not
        #    connected); also drop any pending leave-location entries
        for eff in tuple(self.effects.values()):
            game.effectDisconnect(eff)
            if eff in game._leaveLocationEffectList:
                game._leaveLocationEffectList.remove(eff)
        self.effects.clear()
        self._modifiedEffectList.clear()

        # 2. load the new identity's base data; keep side/location/uniID/equips/buffs.
        #    NOTE: do NOT call reinitAttr() here — it resets side to side_0, which would
        #    desync a controlled monster from the monster list it actually sits in.
        self.loadAttrFromDATA(newKey)
        self.cardType = self.cardType_0
        self._reinitBuffAttr()        # atk/def/attr/race/level -> new base (leaves side/location)

        # 3. build the new card's effects, then reapply existing buffs on the new base
        self.shortEffectsInit()
        self.effectsInit()
        self._autoInitBuiltinEffects()
        self._recalBuffs()

        # 4. connect the new effects for the current location (mirror y_cardChangeLocation)
        for eff in tuple(self.effects.values()):
            observeLocation = eff.observeSignals[0]
            if observeLocation != 0:
                if observeLocation & self.location != 0:
                    game.effectConnect(eff)
                elif eff._OBSERVE_LEAVE_FIELD_SIGNAL:
                    game._leaveLocationEffectList.append(eff)

    def playanimTargetTo(self, cardDataList: [Card]):
        pass

    def stopanimTargetTo(self):
        pass

    def hasLife(self):
        if self.defence==0:
            return False
        if self.atk>self.defence:
            return True
        return False


    def y_becomeHalfLife(self,appendSignals=None):
        if not self.hasLife():
            return
        #atk Changed
        b=CardBuff.attackChange(EFF_DURATION.onceForever)
        b.number=self.defence
        self._addBuff(b)
        self._recalBuffs()
        if appendSignals:
            self.game.appendSignalsByBuffID(appendSignals, b.BUFF_ID, self)
        else:
            appendSignals=[]
            self.game.appendSignalsByBuffID(appendSignals, b.BUFF_ID, self)
            for sig in appendSignals:
                yield self.game.y_sendSignal(sig)

    #return should die
    def checkShouldDieTakeDamage(self,num)->bool:
        if self.getCurNumber()<=num:
           return True
        return False

    #return signals
    def takeDamageBuff(self,damageNumber):
        buff1=defenceAdd(EFF_DURATION.onceForever)
        buff1.number=-damageNumber
        buff2=attackAdd(EFF_DURATION.onceForever)
        buff2.number=-damageNumber
        self._addBuff(buff1)
        self._addBuff(buff2)
        changeDataSignals=[]
        self.game.appendSignalsByBuffID(changeDataSignals, buff1.BUFF_ID, self)
        self.game.appendSignalsByBuffID(changeDataSignals, buff2.BUFF_ID, self)
        self._recalBuffs()

        # if self.isDefence():
        #     buff=defenceAdd(EFF_DURATION.onceForever)
        #     buff.number=-damageNumber
        # else:
        #     buff=attackAdd(EFF_DURATION.onceForever)
        #     buff.number=-damageNumber
        # self._addBuff(buff)
        # changeDataSignals=[]
        # self.game.appendSignalsByBuffID(changeDataSignals, buff.BUFF_ID, self)
        # self._recalBuffs()
        return changeDataSignals


    def isDefence(self):
        return self.form&FORM.defence!=0


    def setShowed(self):
        self.hasShown=True


    def calculateCardPower(self):
        pass

    def logOperation(self):
        operationPanel=self.getDuel().getOperatePanelOfCard(self)
        DEBUG_MSG("avail",operationPanel.availOperates)
        DEBUG_MSG("notavail",operationPanel.notAvailOperates)

    def onDestroy(self):
        for effect in self.effects.values():
            effect.onDestroy()
        self.effects.clear()
        self._modifiedEffectList.clear()
        self.buffList.clear()


class NormalMonster(Card):
    pass
