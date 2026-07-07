# -*- coding: utf-8 -*-


from __future__ import annotations

from KBEngine import *
from b.Card import *
from util import *


from annos import *
from b.Game import Game
from a.Deck import Deck
from decks import decks

"""
Duel:Bridge connecting game logic and client-inputs & client-shows.The core function is y_clientOperate, which accepts players' operations.Game logic is in Game.py, not in Duel.py


MainGameLoop
    clientOperate: receive all players' operations
    onTickDuel: called every 0.2s

"""


class Duel(Reload):
    def __init__(self, duelNode, duelID, avatars,botName=""):
        Reload.__init__(self, True, True)

        self.isDestroyed = False
        ASSERT_MSG(len(avatars) == 2 and 1 in avatars and 2 in avatars, "avatars cnt illegal")

        #---------------------------------------------Players and Watchers
        #the 2 duelers in this duel,key is 1,2
        self.avatars: Dict[int, AvatarCE] = avatars
        #all the spectators,not include duelers
        self.watcherList: List[AvatarCE] = []

        #-----------------------------------------------

        #unique duel id,all the avatars and Monsters have the same c_duelID
        self.duelID: int = duelID

        self.uniIDCnt = 0
        #include all cards be used, uniID:card
        self.usedCards: Dict[int, Card] = {}
        #indicate who's move,time counter
        self.avatarTimes: Dict[int, DuelTimeout] = {}

        self.stage = DUEL_STAGE.none

        # side:LOSE_REASON
        self._losers: Dict[int, LOSE_REASON] = {}
        self.duelEndReason: str = ""

        self.cantUseLog = ""
        self.cantSwitchSide = False

        #----------------------------------config,set to True when debugging
        self.INIT_LP=8000
        self.MAX_HAND_CARD=6
        self.INI_HAND_CARD = 5
        self.SKIP_ROCKPAPERSCI = False
        self.SKIP_SHUFFLE_DECK = False
        self.TEST_SUMMON = False
        self.INFINITE_BATTLE = False
        self.INFINITE_USE_EFFECT = True
        self.IS_TEST_PLAY=False
        #timeout lose
        self.NO_TIMEOUT = True
        #---------------------------------------

        self._lastUpdateTime = 0
        self._botName=botName

        #duel mode of this game: any bot involved -> vsbot, otherwise publicRoomPVP.
        #used to pick the reward table on the base side
        self.duelStartMode = DUEL_START_MODE.publicRoomPVP
        if botName or any(a.c_isBot for a in self.avatars.values()):
            self.duelStartMode = DUEL_START_MODE.vsbot

        #play client shows of this duel
        self.duelNode: DuelNode = duelNode
        self.space: SpaceCE = self.duelNode.space

        #cards need to update to clients
        self.dirtyCards = {}

        self.game: Game = None
        self._makeEnemySideTuple()


        self.IS_TUTORIAL=False
        if list(self.avatars.values())[0].space.cell_worldType==WORLD_TYPE.tutorial:
            self.IS_TUTORIAL=True

        if getIsBHVer():
            self.INIT_LP=4000


    def showDuelStartPreparePanel(self):
        self.stage = DUEL_STAGE.preparing
        self.getNotBotAvatar(1).initAndShowDuelStartPanel(list(self.avatars.values()))

        #remove all result panels of last duel
        for eid,en in entities.items():
            if en.className=="WorldUIPopup":
                worldUI:WorldUIPopupCE=en
                if worldUI.duelPlaceID==self.duelNode.c_duelPlaceClientData.placeID:
                    worldUI.tryDestroy()

        avatar=self.getNotBotAvatar(1)
        if avatar.isDuelWithSelf:
            self.duelNode.c_canSwitchSide=True

        if self._botName==TESTPLAY_BOT:
            self.IS_TEST_PLAY=True
            self.duelNode.c_canSwitchSide=True
            self.startDuel()
        elif self._botName=="tutorialBot":
            self.IS_TUTORIAL=True
            self.startDuel()
            avatar.c_startGuideUI()



    """
        Starting game process
        
        startDuel:
        1) parse player's decks
        
        2) game.initGame()
            prepare decks,create all cards in decks
            
        3) startCoroutine(self.y_startDuel()
            1) start rock paper scissors
            2) self.game.startGameAndDrawStartHand(whoseTurn)
                Distribute player's hands
                start player1's turn
        
    """

    def startDuel(self):
        if self.isDestroyed:
            ERROR_MSG("start Duel destroyed")
            return
        if self.stage not in (DUEL_STAGE.none, DUEL_STAGE.preparing):
            ERROR_MSG("startDuel Error :self.stage != DUEL_STAGE.notingame")
            return

        self.usedCards.clear()
        self._losers.clear()

        ### initialize player decks
        _decks={}
        if self.IS_TUTORIAL:
            self.SKIP_SHUFFLE_DECK=True
            for side,avatar in self.avatars.items():
                if not avatar.c_isBot:
                    _decks[side]=decks.TUTORIAL_DECK
                else:
                    _decks[side]=decks.TUTORIAL_ENEMY_DECK
                    avatar.getDuelAI().shouldWin=False
        else:
            for side,avatar in self.avatars.items():
                if not avatar.c_isBot:
                    _decks[side]=Deck()
                    _decks[side].reinitDeck(avatar.c_curUsedDeck)
                else:
                    _decks[side]=avatar.getBotDeck()

        ASSERT_MSG(self.game == None, "error game!=None while startDuel")
        self.game = Game(self)

        if not self.game.parseDecks(_decks):
            ERROR_MSG("game init failed")
            self.destroy()
            return

        #prepare this duel's win/lose rewards on the base side (AccountFunc) right at duel
        #start; they are actually granted after the duel ends (see gameOverDealWinnerAndLoser)
        if not self.IS_TUTORIAL and not self.IS_TEST_PLAY:
            for side, avatar in self.avatars.items():
                if not avatar.c_isBot and avatar.base:
                    avatar.base.prepareDuelReward(self.duelID, self.duelStartMode)

        self.duelNode.startCoroutine(self.y_startDuel(), True, 0)

    # "y_" means this is a coroutine function
    def y_startDuel(self):
        self.changeStage(DUEL_STAGE.rps)

        yield "wait"
        yield "wait"

        for avatar in list(self.avatars.values()) + self.watcherList:
            self.syncDuel(avatar)
        self.callBotFunc("onDuelStart", self)

        # bot AI 异步初始化(向玩家 base 请求本局赢/输并等待结果)
        for side, avatar in self.avatars.items():
            ai = avatar.getDuelAI()
            if ai:
                initFunc = getattr(ai, "y_initDuelAI", None)
                if initFunc:
                    yield initFunc()


        #-----------------------------init timer
        self.avatarTimes.clear()
        for side, avatar in self.avatars.items():
            isInfinite=False
            if self.NO_TIMEOUT:
                isInfinite=True
            if avatar.c_isBot:
                isInfinite=True
            self.avatarTimes[side] = DuelTimeout(isInfinite)
            self.avatarTimes[side].reinit()
        self.regenTimeoutCount()
        self._lastUpdateTime = time.time()
        #----------------------------------


        if publish():
            flySpeed = 1
        else:
            flySpeed = 3
        if not self.IS_TEST_PLAY:
            self.game.playanimFlyBanner(0, "DUEL START", "",flySpeed)

        #------------------------------------decide who is first
        if self.IS_TEST_PLAY:
            player=self.getNotBotAvatar(1)
            whoseTurn=player.c_side
        elif self.IS_TUTORIAL:
            player=self.getNotBotAvatar(1)
            enemySide=self.getEnemySideTuple(player.c_side)[0]
            whoseTurn=player.c_side
        else:
            whoseTurn = yield self.y_decideWhoisFirst()

        if not self.IS_TEST_PLAY:
            self.game.playanimFlyBanner(whoseTurn,"GOES_FIRST","",flySpeed)
        #-----------------------------------------------------

        self.changeStage(DUEL_STAGE.dueling)

        yield self.game.y_startGameAndDrawStartHands(whoseTurn)

        if self.IS_TUTORIAL:
            yield self.game.y_startTutorialScene()
        elif self.IS_TEST_PLAY:
            yield self.game.y_testScene()


    #return who is first
    def y_decideWhoisFirst(self) -> int:
        whoisfirst = 1
        if self.SKIP_ROCKPAPERSCI or self.duelNode.c_canSwitchSide:
            whoisfirst = self.getNotBotAvatar(1).c_side
        else:
            while 1:
                defaultDict = {
                    1: random.randint(0, 2),
                    2: random.randint(0, 2),
                }
                resultDict = yield self.y_multiPlayersShowPopup(TITLE.decideWhoFirst, "", tuple(self.avatars.keys()),
                                                                ["ROCK", "PAPER", "SCISSORS"],
                                                                defaultDict, "", POPUP_TYPE.rockpaperscissors, timeout=20)
                self.duelNode.playanimRockPaperScissors(resultDict[1], resultDict[2])
                if resultDict[1] == resultDict[2]:
                    continue
                elif (resultDict[1], resultDict[2]) == (0, 2):
                    whoisfirst = 1
                    break
                elif (resultDict[2], resultDict[1]) == (0, 2):
                    whoisfirst = 2
                    break
                elif resultDict[1] < resultDict[2]:
                    whoisfirst = 2
                    break
                else:
                    whoisfirst = 1
                    break

        choice = yield self.y_showPopup(TITLE.decideWhoFirst, "decideWhoFirstTxt", whoisfirst, ["FIRST", "SECOND"],
                                        random.randint(0, 1), "", POPUP_TYPE.normal, timeout=20)

        if choice == 0:
            pass
        else:
            whoisfirst = self.getEnemySideTuple(whoisfirst)[0]

        return whoisfirst

    #rock paper scissors
    def chooseRPS(self, side, rps: int):
        self.duelNode.onCallBack("chooseRPS%d" % side, rps)

    """
    change to notingame or dueling
    """

    def changeStage(self, s: DUEL_STAGE):
        DUEL_MSG("changeDuelStage ", s)
        self.stage = s
        self.getNotBotAvatar(1).duelStartPanelChangeStage(s)

    def regenTimeoutCount(self):
        for side, t in self.avatarTimes.items():
            t.regen()
        self.duelNode.setAvatarTimes(self.avatarTimes)

    """
    called every 0.2s
    """

    def onTickDuel(self):
        if self.stage != DUEL_STAGE.dueling:
            return


        deltaTime = time.time() - self._lastUpdateTime
        self._lastUpdateTime = time.time()

        #-------------------------------check timeout lose
        if not self.hasLoser():
            timeoutSide = 0
            for side, avatarTime in self.avatarTimes.items():
                isTimeout = not avatarTime.costTime(deltaTime)
                if isTimeout and not self.avatars[side].c_isBot:
                    timeoutSide = side
            if timeoutSide:
                self.setLoser(timeoutSide, LOSE_REASON.timeout)

            self.duelNode.setAvatarTimes(self.avatarTimes)
        #----------------------------------


        if self.hasLoser():
            self.duelEnd()

        # if self.timeoutForceTurnEnd:
        #     self.timeoutForceTurnEnd = False
        #     if self.duelNode.hasCoroutine("y_clientOperate"):
        #         ERROR_MSG("TurnEnd self.duelNode.hasCoroutine")
        #         return
        #     self.clientOperate(self.whoseTurn, 0, OPERATE.turnEnds, "")


    """
    callen when avatar spectators or reconnects
    
    sync all duel data to avatar
    
    """

    def syncDuel(self, avatar):
        if self.isDestroyed:
            ERROR_MSG("onSyncDuelEnd but destroyed")
            return

        if not self.game:
            return

        game = self.game

        """
        ask the client to set up the duel,if any of DuelNode or CardEntity not in the client, called onSyncDuelFailed
        """
        allIDs = game.getCardEntityIDList()
        allIDs.append(self.duelNode.id)
        avatar.c_syncDuel(self.duelID, allIDs)

        mySide = avatar.c_side

        for tempside in self.avatars.keys():
            game.syncCardList(tempside, LOCATION.hand, mySide)
            game.syncCardList(tempside, LOCATION.deck, mySide)
            game.syncCardList(tempside, LOCATION.extraDeck, mySide)
            game.syncCardList(tempside, LOCATION.grave, mySide)
            game.syncCardList(tempside, LOCATION.banish, mySide)

        if avatar.c_duelID == 0:
            #this is a watcher
            if avatar not in self.watcherList:
                self.watcherList.append(avatar)
            if self.duelID not in avatar.c_watchDuelIDList:
                avatar.c_watchDuelIDList.append(self.duelID)
            avatar.c_watchDuelIDList = avatar.c_watchDuelIDList
            avatar.removeAllDuelArgs()
        else:
            #this is a dueler
            self.recalculateAllCardsOperation()

    def onSyncDuelFailed(self, avatar):
        if self.isDestroyed:
            return
        if avatar.c_duelID == self.duelID:
            ERROR_MSG("avatar dueler onSyncDuelFailed")
            self.setLoser(avatar.c_side, LOSE_REASON.clientDeath)
        else:
            self.setWatcher(avatar, False)

    def clientOperate(self, side, cardUniID: int, operate: OPERATE, operateArg: str):
        if self.stage != DUEL_STAGE.dueling:
            #TODO rps
            return

        if len(self._losers):
            return

        #anyone could surrender at any moment
        if operate == OPERATE.surrender:
            self.setLoser(side, LOSE_REASON.surrender)
            self.duelNode.stopCoroutine("y_clientOperate", True)
            return

        DEBUG_MSG("clientOperate ", side, getOperateName(operate))

        if side not in self.game.whoCanMove:
            return

        if not self.duelNode.hasCoroutine("y_clientOperate"):
            self.duelNode.startCoroutine(self.y_clientOperate(side, cardUniID, operate, operateArg), True, 0)
        elif self.duelNode.hasStuck("y_clientOperate", "clientSelectedCardOperate%d" % side):
            self.duelNode.onCallBack("clientSelectedCardOperate%d" % side, cardUniID, operate, operateArg)

    """
    deal player's operation,this function is the most important function
    
    "y_" means this is a coroutine,can only be called like "yield y_XXX" in another coroutine
    
    #side : player's side
    #cardUniID: the card player clicked
    #operate : player's operation
    #operateData: extra data of operation
    """

    def y_clientOperate(self, side: int, cardUniID: int, operate: OPERATE, operateData: str):
        if side not in self.avatars:
            return
        avatar = self.avatars[side]  #the operator

        self.game.resetWhoCanMove()
        #only turn player can operate first,other player can't operate first,other player can only trigger effects after the operation
        if side != self.game.whoseTurn:
            return

        if operate not in (OPERATE.click, OPERATE.vrTriggerDown):
            if operate == OPERATE.changePhase:
                yield self.game.y_changePhase()
            elif operate == OPERATE.turnEnds:
                yield self.game.y_turnEnds()
            else:
                WARNING_MSG("unknow operation ", operate)

            self.recalculateAllCardsOperation()
            self.resetSelected(side)
            yield self.game.y_solveTriggerQueue()
            return

        #the selected card
        card = self.cardUniIDToCard(cardUniID)
        #if the card is not legal
        if not card:
            INFO_MSG("click empty")
            self.resetSelected(side)
            return

        #player clicks any card
        INFO_MSG("y_clientOperate click", card.cardKey, getOperateName(operate))

        INFO_MSG("click card ", card.getName())

        #currently,player can only click his own card,player cant activate enemy's card effect
        if card.side != side:
            self.resetSelected(side)
            return

        #get this card's available operations,such as Summon,Activate,Change Form
        availAttackTargetTuple = self.game.player_getAttackTargetListOfCard(card)
        operatePanel = self.getOperatePanelOfCard(card, availAttackTargetTuple)
        if not operatePanel:
            operatePanel = OperatePanel.getNone()

        avatar.c_selectedCard = card
        #make client show selections of operations in front of player
        avatar.c_operatePanel = operatePanel
        #highlight enemies can be attacked
        # self.setTargetLights(side, CARD_LIGHT.targetRed, availAttackTargets)

        #stuck here and wait for player's next operation
        waitResult = yield WaitForCB("clientSelectedCardOperate%d" % side)

        self.resetSelected(side)  #hide operate panel,hide selected card light

        #maybe timeout or turn ends
        if waitResult.called == 0:
            return

        #player's next operation
        cardUniID2, operate2, operateArg2 = waitResult.args
        #the second card player selected
        card2 = self.cardUniIDToCard(cardUniID2)

        self.cantUseLog = ""
        operateSuccess = True

        if operate2 in (OPERATE.click, OPERATE.vrTriggerUp):
            #Clicking on the second card may result in a battle or selecting the second card.

            if not card2 or card == card2:
                self.resetSelected(side)
                return

            triedBattle = False
            #try attack card2
            if card.side == side and card.isMonster() and card.isInMonsterZone() and card2.side != side and card2.isMonster() and card2.isInMonsterZone():
                DUEL_MSG(f"{card.getName()} try attack {card2.getName()}")
                triedBattle = True
                operateSuccess = yield self.game.y_player_monsterAttack(card, card2)

            if triedBattle:
                pass
            elif operate2 == OPERATE.click:
                #player clicks a new card
                self.duelNode.startCoroutine(self.y_clientOperate(side, cardUniID2, operate2, operateArg2),
                                             False, 0)
                return

        elif operate2 == OPERATE.vrTriggerDown:
            WARNING_MSG("shouldn't enter this,player can't press trigger twice without releasing.")
            if card2:
                self.duelNode.startCoroutine(self.y_clientOperate(side, cardUniID2, operate2, operateArg2), False,
                                             0)
            else:
                self.resetSelected(side)
            return


        elif operate2 == OPERATE.normalSummon:

            DUEL_MSG("try normal summon ", card.getName())
            operateSuccess = yield self.game.y_player_normalSummon(False, card,True)

        elif operate2 == OPERATE.extraSummon:
            DUEL_MSG("try extra summon", card.getName())
            operateSuccess = yield self.game.y_player_extraSummonFromExtraDeck(False, card, True)

        elif operate2 == OPERATE.setSpell:
            #set spell card to field
            operateSuccess = yield self.game.y_player_setCardToSpellZone(False, card)

        elif operate2 == OPERATE.returnSetCard:
            #return a face-down set card back to hand
            operateSuccess = yield self.game.y_player_returnSetCardToHand(False, card)

        elif operate2 == OPERATE.directAttack:
            enemySides = availAttackTargetTuple[1]
            # if len(enemySides)>1:
            #     yield self.y_showPopup()

            if len(enemySides) == 1:
                #direct attack enemy player
                operateSuccess = yield self.game.y_player_monsterAttack(card, enemySides[0])

        elif operate2 == OPERATE.rangedAttack:
            yield self.game.y_player_monsterRangedAttack(card)

        elif operate2 in (OPERATE.changeToAttack, OPERATE.changeToDefence):
            yield self.game.y_player_changeMonsterForm(card, operate2)

        elif operate2 == OPERATE.changePhase:
            #player change phase
            yield self.game.y_changePhase()
        elif operate2 == OPERATE.turnEnds:
            yield self.game.y_turnEnds()

        elif OPERATE.activateEffect <= operate2 < OPERATE.activateEffect_end:
            #player use card's effect
            operateSuccess = yield self.game.y_player_activateActiveEffect(side, card, operate2)
        elif operate2 == OPERATE.testSummon:
            yield self.game.y_specialSummon(card)

        if not operateSuccess:
            if self.cantUseLog:
                avatar.c_showLabel(self.cantUseLog)
                if avatar.c_operateType != OPERATE_STYLE.VR:
                    self.duelNode.startCoroutine(self.y_clientOperate(side, cardUniID, operate, operateData), False,
                                                 0)
                    return

        self.recalculateAllCardsOperation()
        self.resetSelected(side)
        yield self.game.y_solveTriggerQueue()

    """
    remove the grabbed card
    hide operation panel
    """

    def resetSelected(self, side):
        self.cantUseLog = ""
        self.avatars[side].c_selectedCard = CardData.getNone()
        self.avatars[side].c_operatePanel = OperatePanel.getNone()
        self.game.resetWhoCanMove()

    #get the card by uniID,return None if not found
    def cardUniIDToCard(self, uniID) -> Card:
        if uniID == 0 or uniID not in self.usedCards:
            return None
        else:
            return self.usedCards[uniID]

    def eachPlayerShowNotify(self, notify: str):
        for side, avatar in self.avatars.items():
            if not avatar.c_isBot and not avatar.isDestroyed:
                avatar.c_showLabel(notify)

        for watcher in self.watcherList:
            watcher.c_showLabel(notify)

    def ________________clientPanel(self):
        pass

    """
    show popup window to a SINGLE player
    
    side:player's side, 1 or 2
    options:list of choices in string
    defaultResult:if timeout or player is bot,return this value
    canCancel:if player clicks the cancel button on joystick,return the last option
    timeout:timeout in seconds,0 means no timeout

    return:the order of choice
    
    for example:
        result = yield self.y_showPopup(TITLE,TEXT,1,['YES','NO'],1)
        
                =======================
                |        TITLE        |
                |                     |
                |         TEXT        |
                |                     |
                |   YES         NO    |
                |                     |
                =======================
                
        result 0->YES 1->NO
            if timeout,return 1
            
            
    "y_" function means it MAY need to wait for player's operation,or MAY NOT
    it must be called like "yield y_showPopup()",whether it has to wait or not
    all functions calling "y_" must also be named "y_" and with "yield" ahead,or
    call it like "entity.startCoroutine(y_XXXXX())"
    if a sync function treated as async and called with "yield" ahead,it had no problem
    if a async function called without a "yield",it went wrong
    """

    def y_showPopup(self, title: str, text: str, side: int, options: List[str], defaultResult: int,cancelOption="",
                    popupType: POPUP_TYPE = 0, reasonCard=None, timeout: float = 0) -> int:
        result = yield self.y_multiPlayersShowPopup(title, text, (side,), options, {side: defaultResult}, cancelOption,
                                                    popupType, timeout)
        return result[side]

    """
    show popup windows to multi players at the same time,for example:RockPaperScissors
         
    return {1:result1,2:result2}
    """

    def y_multiPlayersShowPopup(self, title, text, sideTuple: tuple, options:List[str], defaultResultDict, cancelOption:str="",
                                popupType: POPUP_TYPE = 0, reasonCard=None, timeout: float = 0) -> Dict[int, int]:
        if type(sideTuple) == int:
            ERROR_MSG("y_showMultiPlayerPopup sideTuple not tuple", sideTuple)
            return {sideTuple: 0}

        if not title:
            title = ""
        elif title == TITLE.auto:
            title = self._genAutoTitle()

        canCancel=False
        if cancelOption:
            options=list(options)
            options.append(cancelOption)
            canCancel=True

        self.game.setWhoCanMove(sideTuple)

        #show label
        for side, avatar in self.avatars.items():
            if side not in sideTuple:
                avatar.setStaticLabelShown("waitingForChoose", True,
                                           makeStrNoTrans("waitingForChoose", avatar.c_nickName))

        resultDict = {}
        popupIDSide = {}
        for side in sideTuple:
            resultDict[side] = defaultResultDict[side]

        aibots = {}
        playerWaitDict = {}
        for side in sideTuple:
            avatar = self.avatars[side]
            if avatar.getDuelAI():
                aibots[side] = avatar
                avatar.botCE.setBotAnim(AVATAR_ANIM.deciding, True)
            else:
                popupid = avatar.showPopup(True, title, text, options, "onDuelPopup", "", canCancel,
                                           popupType, timeout,True)
                s = "onDuelPopup%d" % popupid

                playerWaitDict[s] = timeout
                popupIDSide[popupid] = side

        # showLabelAvatars=()
        # for avatar in self.avatars.values():
        #     if avatar.c_side not in sideTuple:
        #         #lan
        #         avatar.setStaticLabelShown(True,"enemyDeciding","enemyDeciding")
        #         showLabelAvatars+=avatar

        if len(playerWaitDict):
            yResult = yield WaitForCB(playerWaitDict)
            for n, waitResult in yResult.items():
                if waitResult.called != 0:
                    popupID = int(n.replace("onDuelPopup", ""))
                    resultDict[popupIDSide[popupID]] = waitResult.args[0]

            for popupid, side in popupIDSide.items():
                self.avatars[side].removePopup(popupid)

        for side, bot in aibots.items():
            botCE: BotAICE = bot
            resultDict[side] = yield botCE.duelAI.y_onShowPopUp(title, text, options, resultDict[side], canCancel,
                                                                popupType,
                                                                reasonCard)
            botCE.setBotAnim(AVATAR_ANIM.deciding, False)

        #hide label
        for side, avatar in self.avatars.items():
            if side not in sideTuple:
                avatar.setStaticLabelShown("waitingForChoose", False)

        self.game.resetWhoCanMove()
        return resultDict

    def onDuelPopup(self, side, popupID: int, result: int, data: str):
        if not self.avatarTimes[side].isMove:
            return
        self.avatarTimes[side].isMove = False
        INFO_MSG("onDuelPopup", result)
        self.duelNode.onCallBack("onDuelPopup%d" % popupID, result)



    def _genAutoTitle(self):
        period, effect = self.game.getDealingEffect()
        title = ""
        if effect:
            if period == EFF_PERIOD.costing:
                title = "title_costing_select"
            else:
                title = "title_activating_select"
        return title

    """
    Request the player to select cards from the cardList,if all cards are in hand or on the field,show laser
    
    side: 1 or 2
    options: ["A","B"]
    cancelOption : "CANCEL" 
    cardList:all cards to choose
    
    legalGroups:[group1OfCards,group2OfCards,...]   list of candidates

    return (option,cardList)
    """

    def y_showCardSelectorPanel(self, cardList: [Card], title: str, side: int, options: List[str], minNum=1, maxNum=1,
                                                            defaultOption: int = None, defaultResult: [CardData] = None, cancelOption:str="",
                                                            hasOrder=False, legalGroups: [[Card]] = None,
                                                            timeout: float = 0) -> Tuple[int, [Card]]:
        if type(side)!=int or side==0 or side not in self.avatars:
            ERROR_MSG("y_showCardSelectorPanel side error ",side)
            return 0,[]
        result=yield self.y_multiPlayersShowCardSelectorPanel({side:cardList},title,(side,),options,minNum,maxNum,{side:defaultOption},{side:defaultResult},cancelOption,hasOrder,{side:legalGroups},{side:timeout},CARD_SELECTOR_TYPE.multiSelector)
        if side not in result:
            return 0,{}
        r=result[side]
        return r[0],r[1]


    """
    show card selector panel to multi players at the same time
    
    cardListDict: {side:[Card]}
    
    sideTuple: (1,2)
    
    options: ["A","B"] or None
    
    defaultOptionDict: {side:0}
    
    cancelOption: "CANCEL"
    
    return {side:(option,cardList,usedTime)}
    """

    def y_multiPlayersShowCardSelectorPanel(self, cardListDict: Dict[int, [Card]], title: str, sideTuple: Tuple,options=None,
                                            minNum=1, maxNum=1, defaultOptionDict=None,defaultResultDict=None,cancelOption="",hasOrder=False, legalGroupsDict=None,timeoutDict = None,selectorType=CARD_SELECTOR_TYPE.multiSelector) -> Dict[
        int, Tuple[int,List[Card],float]]:
        if not title:
            title = ""
        elif title == TITLE.auto:
            title = self._genAutoTitle()


        if not options:
            options=[]
        if cancelOption:
            options=list(options)
            options.append(cancelOption)
        canCancel=cancelOption!=""
        lastOption = len(options) - 1

        if type(sideTuple) != tuple:
            ERROR_MSG("y_multiPlayerShowCardSelectorPanel sideTuple not tuple", sideTuple)
            return {}
        if len(sideTuple)==0:
            return {}

        result={}
        for side in sideTuple:
            if side not in self.avatars:
                ERROR_MSG("y_multiPlayersShowCardSelectorPanel side error", side)
                return {}
            result[side]=lastOption,[],0

        if type(cardListDict) != dict:
            ERROR_MSG("y_multiPlayerShowCardSelectorPanel cardListDict is not dict", cardListDict)
            return result

        for side in sideTuple:
            cardList=cardListDict[side]
            if type(cardList)!=list:
                ERROR_MSG("type(cardList)!=list")
                return result

        #show label
        if len(sideTuple)==1:
            chooseAvatarNickName=self.avatars[sideTuple[0]].c_nickName
            for side, avatar in self.avatars.items():
                if side not in sideTuple:
                    avatar.setStaticLabelShown("waitingForChoose", True,makeStrNoTrans("waitingForChoose", chooseAvatarNickName))
        else:
            for side, avatar in self.avatars.items():
                avatar.setStaticLabelShown("waitingForChoose", True,"waitingForChooseMulti")

        uiID=self.genUniID()

        aibots = {}
        playerWaitDict = {}
        tempDict={} # minNum maxNum
        for side in sideTuple:
            cardList = copy.copy(cardListDict[side])

            tempMinNum=minNum
            tempMaxNum=maxNum
            if tempMaxNum < 0 or tempMinNum > tempMaxNum:
                ERROR_MSG("y_multiPlayersShowCardSelectorPanel num error ", minNum, maxNum)
                tempMinNum=tempMaxNum

            legalGroups=None
            if legalGroupsDict and side in legalGroupsDict:
                legalGroups=legalGroupsDict[side]
                if not legalGroups:
                    if tempMinNum > len(cardList):
                        tempMinNum = len(cardList)

                    if tempMaxNum > len(cardList):
                        tempMaxNum = len(cardList)
                else:
                    tempMaxNum=-1
                    tempMinNum=-1

            legalGroupsLength = 0
            if legalGroups: #changed to uid
                legalGroups = [[card.uniID for card in sublist] for sublist in legalGroups]
                for l in legalGroups:
                    l.sort()
                    legalGroupsLength += len(l)
                if canCancel:
                    legalGroups.append([])

            defaultResult=None
            if defaultResultDict and side in defaultResultDict:
                defaultResult=defaultResultDict[side]
            if not defaultResult:
                defaultResult=[]
                if not canCancel:
                    for i in range(tempMinNum):
                        defaultResult.append(cardList[i])

            option=None
            if defaultOptionDict and side in defaultOptionDict:
                option=defaultOptionDict[side]
            if not option:
                option=lastOption

            if hasOrder and legalGroups:
                ERROR_MSG("hasOrder and legalGroups")

            timeout=0
            if timeoutDict and side in timeoutDict:
                timeout=timeoutDict[side]

            tempDict[side]={}
            tempDict[side]["minNum"]=tempMinNum
            tempDict[side]["maxNum"]=tempMaxNum
            tempDict[side]["legalGroups"]=legalGroups

            result[side]=option,defaultResult,timeout+1


            avatar = self.avatars[side]
            if avatar.getDuelAI():
                aibots[side] = avatar
                avatar.botCE.setBotAnim(AVATAR_ANIM.deciding, True)
            else:
                d = CardSelectorData()
                d.uiID=uiID
                d.isEnabled = True
                d.text = title
                d.options = options
                if len(cardList) > 400:
                    ERROR_MSG("y_multiPlayerShowCardSelectorPanel len(cardList)>400 ,this is impossible")
                    cardList = cardList[0:400]
                d.cardList = cardList
                if legalGroups == None or legalGroupsLength > 10000:
                    d.legalGroups = []
                else:
                    d.legalGroups = legalGroups
                d.hasOrder = hasOrder
                d.canCancel = canCancel
                d.minNum = tempMinNum
                d.maxNum = tempMaxNum
                d.paraID=0
                d.cardSelectorType=selectorType
                d.cardEntityID=0
                d.countDownTime=timeout
                avatar.c_cardSelectorPanel = d

                playerTimeout=timeout
                if playerTimeout!=0:
                    playerTimeout+=10
                playerWaitDict["e_cardSelectorResult%d" % avatar.c_side] =playerTimeout
                for card in cardList:
                    if card.form & FORM.set==0:
                        card.setShowed()

        cnnt=0
        while True:
            if len(playerWaitDict)==0:
                break
            cnnt+=1
            whocanMoveSides=[]
            for n in playerWaitDict:
                side=int(n.replace("e_cardSelectorResult", ""))
                whocanMoveSides.append(side)
                avatar=self.avatars[side]
                if cnnt!=1:
                    avatar.c_cardSelectorPanel=avatar.c_cardSelectorPanel
            self.game.setWhoCanMove(tuple(whocanMoveSides)+tuple(aibots.keys()))

            yResult = yield WaitForCB(playerWaitDict)
            for n, waitResult in yResult.items():
                side = int(n.replace("e_cardSelectorResult", ""))
                avatar=self.avatars[side]
                if waitResult.called != 0:
                    resultOption=waitResult.args[0]
                    resultUniIDList = list(set(waitResult.args[1]))
                    usedTime=waitResult.args[2]

                    legalGroups=tempDict[side]["legalGroups"]
                    if legalGroups and len(legalGroups):
                        resultUniIDList.sort()
                        if resultUniIDList not in legalGroups:
                            #client sent cardGroup not legal,try again
                            avatar.c_showLabel("invalidCardGroup")
                            continue

                    minNum=tempDict[side]['minNum']
                    maxNum=tempDict[side]['maxNum']
                    if (minNum>=0 and len(resultUniIDList) < minNum) or (0 <= maxNum < len(resultUniIDList)):
                        TEMP_ERROR("len(resultUniIDList) < tempDict[side]['minNum'] or len(resultUniIDList) > te:",resultUniIDList,tempDict[side])
                        avatar.c_showLabel("invalidResult")
                        continue

                    isResultLegal = True
                    cardList = cardListDict[side]
                    r=[]
                    for uniID in resultUniIDList:
                        card = self.cardUniIDToCard(uniID)
                        if card == None or card not in cardList:
                            isResultLegal = False
                            break
                        r.append(card)
                    if not isResultLegal:
                        avatar.c_showLabel("invalidResult")
                        continue
                    result[side] = resultOption,r,usedTime
                del playerWaitDict["e_cardSelectorResult%d" % side]
                avatar.closeCardSelectorPanel()

        for side, avatar in aibots.items():
            legalGroups=None
            if legalGroupsDict and side in legalGroupsDict:
                legalGroups=legalGroupsDict[side]

            option, resultList = yield avatar.getDuelAI().y_onShowCardSelectorPanel(title, options, cardListDict[side],
                                                                                    minNum, maxNum, result[side][0], result[side][1], canCancel, hasOrder, legalGroups, result)
            result[side] = option,resultList,0
            avatar.botCE.setBotAnim(AVATAR_ANIM.deciding, False)

        self.game.resetWhoCanMove()


        if len(sideTuple)==1:
            for side, avatar in self.avatars.items():
                if side not in sideTuple:
                    avatar.setStaticLabelShown("waitingForChoose", False)
        else:
            for side, avatar in self.avatars.items():
                avatar.setStaticLabelShown("waitingForChoose", False)

        return result

    """
    request player to choose only 1 card from field and his hand cards,dont call this function in card effects
    """

    def y_showFieldHandSelector(self, cardList: [CardData], title, side, defaultResult: Card = None, canCancel=False,
                                timeout: float = 0) -> Card:

        if not title:
            title = ""
        elif title == TITLE.auto:
            title = self._genAutoTitle()

        if type(cardList) != list:
            ERROR_MSG("y_showFieldHandSelector type(cardList)!=list")
            return None

        if len(cardList) == 0:
            ERROR_MSG("y_showFieldHandSelector no card")
            return None

        if not defaultResult:
            defaultResult = cardList[0]

        self.game.setWhoCanMove(side)

        if not title:
            title = "pleaseSelectTarget"
        for tside, tavatar in self.avatars.items():
            if tside == side:
                tavatar.setStaticLabelShown("y_showFieldHandSelector", True, title)
            else:
                tavatar.setStaticLabelShown("waitingForChoose", True,
                                            makeStrNoTrans("waitingForChoose", tavatar.c_nickName))

        avatar = self.avatars[side]
        returnResult = None
        if avatar.getDuelAI():
            avatar.botCE.setBotAnim(AVATAR_ANIM.deciding, True)
            if canCancel:
                options = ["OK", "CANCEL"]
            else:
                options = ["OK"]
            optionInt, l = yield avatar.getDuelAI().y_onShowCardSelectorPanel(title, options, cardList, 1, 1, 0,
                                                                              defaultResult,
                                                                              canCancel, False, None, None)
            avatar = self.avatars[side]
            avatar.botCE.setBotAnim(AVATAR_ANIM.deciding, False)

            if optionInt == 1 or len(l) == 0:
                returnResult = None
            else:
                returnResult = l[0]
        else:
            fieldHandSelectData = FieldHandSelectData()
            fieldHandSelectData.isEnabled = True
            fieldHandSelectData.canCancel = canCancel
            cardUniIDList = [card.uniID for card in cardList]
            fieldHandSelectData.cardUniIDList = cardUniIDList
            self.setTargetLights(side, CARD_LIGHT.targetYellow, cardList)
            avatar.c_fieldHandSelectLaser = fieldHandSelectData

            while 1:
                result = yield WaitForCB("clientSelectedCardOperate%d" % side, timeout)
                avatar = self.avatars[side]
                if result.called == 0:
                    if canCancel:
                        returnResult = None
                    else:
                        returnResult = defaultResult
                    break
                else:
                    cardUniID, operate, operateArg = result.args
                    if operate == OPERATE.cancel and canCancel:
                        returnResult = None
                        break
                    elif operate in (OPERATE.vrTriggerUp, OPERATE.click) and cardUniID in cardUniIDList:
                        returnResult = self.cardUniIDToCard(cardUniID)
                        break

            fieldHandSelectData.isEnabled = False
            fieldHandSelectData.cardUniIDList = []
            avatar.c_fieldHandSelectLaser = fieldHandSelectData
            self.clearTargetLights(side)

        # if returnResult:
        #     en = returnResult.getCardEntity()
        #     if en:
        #         en.c_playanimBeSelected(side)

        for tside, tavatar in self.avatars.items():
            if tside == side:
                tavatar.setStaticLabelShown("y_showFieldHandSelector", False)
            else:
                tavatar.setStaticLabelShown("waitingForChoose", False)

        self.game.resetWhoCanMove()
        return returnResult

    def ________________clientPanelEnd(self):
        pass


    def getPlayerAI(self, side)->DuelAIBase:
        return self.avatars[side].getDuelAI()

    def isDuelWithAI(self):
        playerNum=0
        botNum=0
        for side in self.avatars:
            if self.getPlayerAI(side):
                botNum+=1
            else:
                playerNum+=1
        if playerNum<=1:
            return True
        return False

    def switchAvatarSide(self):
        if not self.duelNode.c_canSwitchSide:
            return
        if self.cantSwitchSide:
            return

        self.avatars[1].botCE.setDuelAI(None)
        self.avatars[2].botCE.setDuelAI(None)
        self.avatars[1].switchDuelArgs(self.avatars[2])
        self.avatars[1], self.avatars[2] = self.avatars[2], self.avatars[1]
        self.duelNode.switchAvatars()
        self.avatars[1].setPosToDuelPlaceSide(1, self.duelNode.c_duelPlaceClientData)
        self.avatars[2].setPosToDuelPlaceSide(2, self.duelNode.c_duelPlaceClientData)

        self.syncDuel(self.avatars[1])
        self.syncDuel(self.avatars[2])

    def callBotFunc(self, funcName, *args):
        for side, avatar in self.avatars.items():
            ai = avatar.getDuelAI()
            if ai:
                func = getattr(ai, funcName, None)
                if not func:
                    ERROR_MSG("ai not found function ", funcName)
                else:
                    func(*args)



    def y_sendSignalToAvatars(self, signal):
        for avatar in tuple(self.avatars.values()):
            ai: DuelAIBase = avatar.getDuelAI()
            if ai:
                yield ai.y_signal(signal)


    def ________________showMonsterOnClient(self):
        pass

    def _setWhoCanMove(self,sideTuple):
        for side, avatarTime in self.avatarTimes.items():
            if side in sideTuple:
                avatarTime.isMove = True
            else:
                avatarTime.isMove = False
        self.duelNode.setWhoCanMove(sideTuple)

    #get the avatar with client
    def getNotBotAvatar(self, preferSide) -> AvatarCE:
        avatar = self.avatars[preferSide]
        if not avatar.c_isBot and avatar.client:
            return avatar
        for side, avatar in self.avatars.items():
            if preferSide != side and not avatar.c_isBot and avatar.client:
                return avatar
        return None

    def getNotBotAvatarBase(self, preferSide):
        avatar = self.getNotBotAvatar(preferSide)
        if not avatar:
            return None
        return avatar.base

    def _checkCardEntitiesControlledBy(self, controlledBy):
        for side in self.game.monsters:
            for card in self.game.monsters[side] + self.game.spells[side]:
                en = card.getCardEntity()
                if not en:
                    ERROR_MSG("_checkCardEntitiesControlledBy not found cardEntity")
                else:
                    if not en.controlledBy:
                        en.controlledBy = controlledBy


    """
    summon a monster to the field or location a spell card on field,then everyone can see it
    
    usage:
        yield y_playCardToField(card)
    
    """

    def y_cardEntityEnterField(self, card: Card, fxID: FX_ID):
        self.cantSwitchSide = True
        #if already has entity,destroy it
        cardEntity = card.getCardEntity()
        if cardEntity:
            ERROR_MSG("card enters field but already has cardEntity ", card.getName())
            cardEntity.mc_playanimFx(FX_ID.none, ANIM.disappear)
            card.entityID = 0
            yield "wait"
            cardEntity.tryDestroy()

        side = card.side

        #random pos and rot
        if side == 1:
            newPos = Vector3(self.duelNode.c_duelPlaceClientData.p1.pos)
            newRad = self.duelNode.c_duelPlaceClientData.p1.radv3.y
        else:
            newPos = Vector3(self.duelNode.c_duelPlaceClientData.p2.pos)
            newRad = self.duelNode.c_duelPlaceClientData.p2.radv3.y
        newPos.z += random.uniform(-3, 3)

        #create the entity that can be seen by clients
        cardEntity: CardEntityCE = self.space.createObj("CardEntity", newPos, Vector3(0, newRad, 0),
                                                        initParas={
                                                            "c_duelID": self.duelID
                                                        })
        cardEntity.initCardEntity(card)
        card.entityID = cardEntity.id

        avatarBase = self.getNotBotAvatarBase(self.getEnemySideTuple(side)[0])
        cardEntity.controlledBy = avatarBase
        self._checkCardEntitiesControlledBy(avatarBase)
        self.duelNode.playanimCardEntityEnterField(cardEntity.id, fxID)

        #wait for the entity sent to clients,if an entity is created and then destroyed in the same frame,it wont be sent to clients,so yield "wait" is necessary
        yield "wait"
        yield "wait"

        self.cantSwitchSide = False


    def cardEntityLeaveField(self, cardEntity:CardEntityCE):
        if not cardEntity.isPlayingLeavingAnim:
            ERROR_MSG("card leaves field without playing animation")
            cardEntity.mc_playanimFx(FX_ID.none, ANIM.disappear)

        self.duelNode.c_cardEntityDestroy(cardEntity.id)
        cardEntity.tryDestroy()


    # def y_cardEntityResetPosition(self, cardEntity: CardEntityCE, shouldShowTeleportAura=False):
    #     side = cardEntity.c_cardData.side
    #
    #     if cardEntity.c_cardData.location & LOCATION.mask_onField ==0:
    #         ERROR_MSG("y_playCardToField cardPlace error")
    #         return
    #
    #     isSuccess = False
    #     controller = self.getNotBotAvatar(side)
    #     if controller:
    #         self.cantSwitchSide=True
    #         self._setCardEntitiesControlledBy(side, controller.base)
    #         controller.c_resetPlaceOfControlledCardEntity([cardEntity.id])
    #
    #         cbResult = yield WaitForCB("e_resetPlaceOfCardEntitySuccess%d" % controller.id, 2)
    #         if cbResult.called > 0:
    #             isSuccess = True
    #             yield "wait"  #wait for pos and rot to send to server
    #             yield "wait"
    #         else:
    #             ERROR_MSG("y_cardEntityChangePlace timeout")
    #     else:
    #         ERROR_MSG("y_cardEntityChangePlace no avail client")
    #
    #     self._setCardEntitiesControlledBy(side,None)
    #
    #     #set monster pos failed,randomly set a pos
    #     if not isSuccess:
    #         if side == 1:
    #             newPos = self.duelNode.c_duelPlaceClientData.p1.pos
    #             newRad = self.duelNode.c_duelPlaceClientData.p1.radv3
    #         else:
    #             newPos = self.duelNode.c_duelPlaceClientData.p2.pos
    #             newRad = self.duelNode.c_duelPlaceClientData.p2.radv3
    #         newPos.x += random.uniform(-3, 3)
    #         cardEntity.setPos(newPos)
    #         cardEntity.setRad(Vector3(0, newRad, 0))
    #     self.duelNode.playanimAllCardEntitySyncPosAndRot(cardEntity.id)
    #
    #     self.cantSwitchSide=False

    def ________________showMonsterOnClientEnd(self):
        pass

    def _________________cardLight(self):
        pass

    """
    get available and not available operations of the card 
    """

    def getOperatePanelOfCard(self, card, availAttackTargetTuple=None) -> Union[OperatePanel, None]:
        canattackMonstersList = None
        canattackPlayersList = None
        if availAttackTargetTuple:
            canattackMonstersList = availAttackTargetTuple[0]
            canattackPlayersList = availAttackTargetTuple[1]

        availOperates,notAvailOperates = self.game.player_getCardAllOperations(card)
        if canattackPlayersList:
            availOperates.append(OPERATE.directAttack)
        if not notAvailOperates and not availOperates: #None
            if canattackMonstersList:
                operatePanel = OperatePanel()
                operatePanel.cardUniID = card.uniID
                operatePanel.availOperates = []
                operatePanel.notAvailOperates = []
                operatePanel.attackTargetUIDList = [m.uniID for m in canattackMonstersList]
                return operatePanel
            else:
                return None

        availOperates.sort()
        notAvailOperates.sort()

        operatePanel = OperatePanel()
        operatePanel.cardUniID = card.uniID
        operatePanel.availOperates = availOperates
        operatePanel.notAvailOperates = notAvailOperates
        if canattackMonstersList:
            operatePanel.attackTargetUIDList = [m.uniID for m in canattackMonstersList]
        else:
            operatePanel.attackTargetUIDList = []
        return operatePanel

    """
    recalculate operation panel of all cards   
    """

    def recalculateAllCardsOperation(self):
        game = self.game

        for side, avatar in self.avatars.items():
            if side not in game.whoCanMove:
                avatar.setCardOperationList([])
            else:
                cardAvailOpList = []

                for card in game.monsters[side]:
                    availAttackTargetTuple = self.game.player_getAttackTargetListOfCard(card)
                    p = self.getOperatePanelOfCard(card, availAttackTargetTuple)
                    if p:
                        cardAvailOpList.append(p)

                for card in game.spells[side] + game.hands[side] + game.extraDecks[side] + \
                            game.graves[side] + game.banishes[side]:
                    p = self.getOperatePanelOfCard(card)
                    if p:
                        cardAvailOpList.append(p)

                avatar.setCardOperationList(cardAvailOpList)

    """
    enemy cards can be attacked
    """

    def setTargetLights(self, side, light: CARD_LIGHT, cardList: [Card]):
        if light not in (CARD_LIGHT.targetRed, CARD_LIGHT.targetYellow, CARD_LIGHT.targetWhite):
            ERROR_MSG("setTargetLights illegal ", light)
            light = CARD_LIGHT.targetYellow
        targetLights = {}
        for card in cardList:
            targetLights[card.uniID] = light
        self.avatars[side].setTargetLights(targetLights)

    def clearTargetLights(self, side):
        self.avatars[side].setTargetLights({})

    def getCantUseLog(self, operate, cardUniID) -> str:
        card = self.cardUniIDToCard(cardUniID)
        if not card:
            return ""
        self.cantUseLog = ""
        if operate == OPERATE.normalSummon:
            getBoolYieldReturn(self.game.y_player_normalSummon(True, card,True))
        elif operate == OPERATE.extraSummon:
            getBoolYieldReturn(self.game.y_player_extraSummonFromExtraDeck(True, card, True))
        elif operate == OPERATE.setSpell:
            getBoolYieldReturn(self.game.y_player_setCardToSpellZone(True, card))
        elif operate == OPERATE.activateEffect:
            self.game.player_getCardCanActivateEffectList(card)
        return self.cantUseLog

    def _________________cardLightEnd(self):
        pass

    def askAvatarDisconnect(self, disconnectSide):
        if self.stage==DUEL_STAGE.dueling or self.stage==DUEL_STAGE.rps:
            for tside in self.getEnemySideTuple(disconnectSide):
                avatar=self.avatars[tside]
                if not avatar.getDuelAI():
                    avatar.showPopup(False,"enemyDisconnected","enemyDisconnectedChoice",["WIN","WAIT"],"onCBaskAvatarDisconnect",str(disconnectSide),False)


    def setWatcher(self, avatar: AvatarCE, isEnable):
        if self.isDestroyed:
            return
        if avatar in self.avatars.values():
            return

        if isEnable:
            self.syncDuel(avatar)
        else:
            if avatar in self.watcherList:
                self.watcherList.remove(avatar)
            if self.duelID in avatar.c_watchDuelIDList:
                avatar.c_watchDuelIDList.remove(self.duelID)
                avatar.c_watchDuelIDList = avatar.c_watchDuelIDList

    def setLoser(self, sideOrTuple: Union[int, tuple], loseReason: LOSE_REASON):
        if not loseReason:
            loseReason = LOSE_REASON.surrender

        if type(sideOrTuple) == int:
            sideOrTuple = (sideOrTuple,)
        for side in sideOrTuple:
            self._losers[side] = loseReason
            DUEL_MSG("setLoser ", self.avatars[side].c_nickName, loseReason)

    def hasLoser(self):
        return len(self._losers)

    """
    duel ends and show result panel,then wait for some seconds,then destroy
    """

    def duelEnd(self):
        DUEL_MSG("duelEnd")
        self.changeStage(DUEL_STAGE.stopping)
        self.duelNode.stopCoroutine("y_clientOperate", True)
        self.duelNode.stopCoroutine("y_bot_operateRepeat", True)
        self.duelNode.stopCoroutine("y_startDuel", True)

        self.gameOverDealWinnerAndLoser()

        self.duelNode.startCoroutine(self.y_duelEnd(True, 60), True, 0)

    # def gameOverDealWinnerAndLoser(self):
    #     if len(self._losers):
    #         if len(self._losers)==1:
    #             loserSide=list(self._losers.keys())[0]
    #             winnerName=self.avatars[3-loserSide].c_nickName
    #             loserName=self.avatars[loserSide].c_nickName
    #             loseReason=self._losers[loserSide]
    #             j={
    #                 "key":"winneris",
    #                 "s0":winnerName,
    #                 "s1t":loseReason
    #             }
    #             text=json.dumps(j)
    #         else:
    #             text="nowinner"
    #         for avatar in list(self.avatars.values())+self.watcherList:
    #             if not avatar.c_isBot:
    #                 avatar.showPopup(False,"duelend",text,["OK"],waitForAnim=True)

    def gameOverDealWinnerAndLoser(self):
        if len(self._losers):
            #notify bot AIs the duel ended (no-op by default)
            self.callBotFunc("onDuelEnd", self)

            isDraw = False

            if len(self._losers) == 1:
                pass
            else:
                isDraw = True

            loseReasonTxt = list(self._losers.values())[0]

            for avatar in list(self.avatars.values()):
                if avatar.c_isBot:
                    worldUILife=10
                else:
                    worldUILife=5*60

                worldUI: WorldUIPopupCE = self.duelNode.space.createObj("WorldUIPopup", avatar.position)
                winOrLose = 1
                if isDraw:
                    winOrLose = 0
                    avatarLoseReasonTxt = loseReasonTxt + "_draw"
                else:
                    if avatar.c_side in self._losers:
                        winOrLose = -1
                        avatarLoseReasonTxt = loseReasonTxt + "_lose"
                    else:
                        winOrLose = 1
                        avatarLoseReasonTxt = loseReasonTxt + "_win"

                #one interface at duel end: report the actual outcome (win/lose pool,
                #bot duels only) AND grant the reward prepared at duel start. All decided
                #by AccountFunc; avatarBA keeps the granted result as a temp for the
                #gameover panel to fetch. duelStartMode tells bot duel from PVP.
                #called BEFORE initGameoverPanel so the panel's fetch reaches base
                #after the temp is written (mailbox calls to the same base are ordered)
                if not isTestDev() and not avatar.c_isBot and avatar.base:
                    intendedShouldWin = False
                    enemy = self.avatars.get(3 - avatar.c_side)
                    if enemy is not None and enemy.c_isBot:
                        ai = enemy.getDuelAI()
                        if ai:
                            intendedShouldWin = bool(ai.shouldWin)
                    avatar.base.reportDuelOutcome(self.duelID, self.duelStartMode, winOrLose,
                                                  avatarLoseReasonTxt, intendedShouldWin)

                worldUI.initGameoverPanel(avatar.id, self.duelID,self.duelNode.c_duelPlaceClientData.placeID,worldUILife, winOrLose, avatarLoseReasonTxt)

    def y_duelEnd(self, shouldDestroy, longestWaitForClientTime):
        #wait client play remain anim
        for eid,avatar in self.avatars.items():
            avatar.playanimDuelEnd()
        yield WaitForCB("e_duelEnd",longestWaitForClientTime)
        self.changeStage(DUEL_STAGE.none)
        yield WaitForSeconds(5)
        DUEL_MSG("stop duel monsters disappear")

        if shouldDestroy:
            self.destroy()
        else:
            for side, avatar in self.avatars.items():
                avatar.removeAllDuelArgs()
            self._clearField()

    #destroy all monsters and spells
    def _clearField(self):
        for cardUniID, card in self.usedCards.items():
            if card.entityID != 0 and card.entityID in entities:
                en = entities[card.entityID]
                en.c_duelID = 0
                en.tryDestroy()

    #immediately destroy this duel in this frame,destroy all monsters
    def destroy(self, clientDeathSide=0, popNotify=""):
        if self.isDestroyed:
            return

        if clientDeathSide:
            popNotify = ""

        if clientDeathSide and self.stage in (DUEL_STAGE.dueling, DUEL_STAGE.rps):
            self.setLoser(clientDeathSide, LOSE_REASON.clientDeath)
            self.gameOverDealWinnerAndLoser()

        self.isDestroyed = True

        for side, avatar in self.avatars.items():
            avatar.c_duelID = 0
            avatar.c_side = 0
            avatar.removeAllDuelArgs()
            if not avatar.c_isBot:
                if popNotify:
                    avatar.showPopupWithOK(popNotify, "", "")
                elif self._botName:
                    avatar.c_setMainPanelEnabled(True)
                    if getIsBHVer():
                        avatar.base.loginToIdleScene()


        for avatar in self.watcherList:
            if popNotify:
                avatar.c_showLabel(popNotify)
            if self.duelID in avatar.c_watchDuelIDList:
                avatar.c_watchDuelIDList.remove(self.duelID)
                avatar.c_watchDuelIDList = avatar.c_watchDuelIDList
        self.watcherList.clear()

        self._clearField()
        self.space.destroyDuel(self.duelID)

    def genUniID(self):
        self.uniIDCnt += 1
        return self.uniIDCnt

    def shuffleUsedCardsUniID(self):
        if self.stage == DUEL_STAGE.dueling:
            ERROR_MSG("dont shuffle uniID in dueling")
            return
        l = list(self.usedCards.values())
        random.shuffle(l)
        self.usedCards.clear()
        for card in l:
            self.uniIDCnt += random.randint(0, 500)
            card.uniID = self.uniIDCnt
            self.usedCards[card.uniID] = card

    def _makeEnemySideTuple(self):
        self._enemySideTuple={}
        self._allySideTuple={}
        for side in self.avatars.keys():
            self._enemySideTuple[side]=tuple([key for key in self.avatars.keys() if key % 2 != side%2])

        for side in self.avatars.keys():
            self._allySideTuple[side]=tuple([key for key in self.avatars.keys() if key % 2 == side%2])

    """
    if 1v1 , self._enemySideTuple={1:(2,),2:(1,)}
    if 2v2 , self._enemySideTuple={1:(2,4),2:(1,3),3:(2,4),4:(1,3)}
    """
    def getEnemySideTuple(self,side):
        return self._enemySideTuple[side]

    def getAllySideTuple(self,side):
        return self._allySideTuple[side]


    def onDestroy(self):
        """
        clean after destroy
        """
        for uniID, card in self.usedCards.items():
            card.onDestroy()
        self.usedCards.clear()
        if self.game:
            self.game.onDestroy()
            self.game = None

        if checkEntityValid(self.duelNode):
            self.duelNode.c_duelID = 0
            self.duelNode.tryDestroy()
            self.duelNode = None

        self.isDestroyed = True
        self.space = None
        self.duelNode = None
        self.avatars.clear()

    def ______________________debugcommand(self):
        pass

    def testmonster(self):
        self.duelNode.startCoroutine(self.y_testmonster(), timeout=0)

    def testLose(self):
        playerSide=self.getNotBotAvatar(1).c_side
        self.game.damagePlayer(playerSide,999999999,False)

    def testWin(self):
        playerSide=self.getNotBotAvatar(1).c_side
        self.game.damagePlayer(3-playerSide,999999999,False)

    def y_clearField(self):
        allCards = self.game.monsters[1] + self.game.monsters[2] + self.game.spells[1] + self.game.spells[2]
        for card in allCards:
            yield self.game._y_changeCardLocation(card, LOCATION.none)

    def y_clearGraveBanish(self):
        allCards = self.game.graves[1] + self.game.graves[2] + self.game.banishes[1] + self.game.banishes[2]
        for card in allCards:
            yield self.game._y_changeCardLocation(card, LOCATION.none)

    def y_clearHand(self):
        allCards = self.game.hands[1] + self.game.hands[2]
        for card in allCards:
            yield self.game._y_changeCardLocation(card, LOCATION.none)

    def y_clearDecks(self):
        allCards = self.game.decks[1] + self.game.decks[2]
        for card in allCards:
            yield self.game._y_changeCardLocation(card, LOCATION.none)

    def y_clearExtraDecks(self):
        allCards = self.game.extraDecks[1] + self.game.extraDecks[2]
        for card in allCards:
            yield self.game._y_changeCardLocation(card, LOCATION.none)

    def y_testAddCard(self, side, cardKey, location):
        card = self.game.createCard(cardKey, side)
        yield self.game._y_changeCardLocation(card, location)

    def y_testSetSpell(self, side, cardKey):
        pass

    def getCardByKey(self, key) -> Card:
        for uid, card in self.usedCards.items():
            if card.cardKey == key:
                return card

    def testcor(self, corFuncName, *args):
        if self.duelNode.hasAnyCoroutine():
            ERROR_MSG("self.duelNode.hasAnyCoroutine")
            return
        self.duelNode.startCoroutine(getattr(self.game, corFuncName)(*args), timeout=0)

    def testChoose(self):
        self.duelNode.startCoroutine(self.y_testChoose(), timeout=0)

    def y_testChoose(self):
        side = self.getNotBotAvatar(1).c_side
        targetSide = 3 - side
        cardList = self.game.hands[targetSide]
        resultL = yield self.game.y_selectCards(cardList, "ttttt", side, 1, 1, canCancel=True)
        print("result=", resultL)

    def y_testPanel(self):
        side = self.getNotBotAvatar(1).c_side
        resultL = yield self.game.y_showYesNoPopUp("eeeeee", "aaaaaa", side)
        print("result=", resultL)

    def y_testBattle(self):
        attackerSide = self.getNotBotAvatar(1).c_side
        attacker = self.game.monsters[attackerSide][0]
        receiver = self.game.monsters[3 - attackerSide][0]
        yield self.game.y_battle(attacker, receiver)

    def y_testReturnToHand(self):
        side = self.getNotBotAvatar(1).c_side
        # yield self.game.monsters[side][0].y_returnToHand(0)

    def testDestroy(self):
        monList = self.game.searchCards(LOCATION.monsterZone)
        mon = monList[0]
        self.duelNode.startCoroutine(self.game.y_destroyCard(mon))

    def testBanish(self):
        monList = self.game.searchCards(LOCATION.monsterZone)
        mon = monList[0]
        self.duelNode.startCoroutine(self.game.y_banishCard(mon))

    def testReturnToHand(self):
        monList = self.game.searchCards(LOCATION.monsterZone)
        mon = monList[0]
        self.duelNode.startCoroutine(self.game.y_returnCardToHand(mon))

    def testReturnToDeck(self):
        monList = self.game.searchCards(LOCATION.monsterZone)
        mon = monList[0]
        self.duelNode.startCoroutine(self.game.y_returnCardToDeck(mon))

    def testSendCardToGrave(self):
        monList = self.game.searchCards(LOCATION.monsterZone)
        mon = monList[0]
        self.duelNode.startCoroutine(self.game.y_sendCardToGrave(mon))

    def testCardReturnToHand(self):
        monList = self.game.searchCards(LOCATION.monsterZone)
        mon = monList[0]
        self.duelNode.startCoroutine(self.game.y_returnCardToHand(mon))


    def ______________________debugcommandEnd(self):
        pass


#timeout countdown
class DuelTimeout:
    isMove = False
    regenTime = 0
    consumedTime = 0
    isInfinite=False

    def __init__(self,_isInfinite=False):
        self.isInfinite=_isInfinite
        self.reinit()

    def reinit(self):
        self.isMove = False
        self.regenTime = 80
        self.consumedTime = 220

    #timeout return false
    def costTime(self, t: float):
        if not self.isMove:
            return True

        if self.isInfinite:
            return True

        if self.regenTime > 0:
            self.regenTime -= t
            if self.regenTime < 0:
                self.regenTime = 0
            return True
        else:
            self.consumedTime -= t
            if self.consumedTime < 0:
                self.consumedTime = 0
                return False
            return True

    def regen(self):
        self.regenTime = 80
        self.consumedTime += 5
        if self.consumedTime > 220:
            self.consumedTime = 220

    def getAll(self):
        if self.isInfinite:
            return 65535
        return self.regenTime + self.consumedTime
