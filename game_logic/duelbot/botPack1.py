# -*- coding: utf-8 -*-
from __future__ import annotations

from util import *
from annos import *
from a.DuelConstants import *
from a import Signal
from decks import decks
from KBEngine import *

# def signBotDecks

"""
logic
================================================================================
AI 决斗整体逻辑 (DuelAINormal)
================================================================================

【核心设计】"娱乐型" AI: 不追求最优解, 而是按预设节奏给玩家输出体验。
每一局开局时根据 MENU_BOTS 中的 botWinRate 概率决定 self.shouldWin (赢/输),
之后所有决策都围绕这个标志运行。

【一局流程】
1. onDuelStart:
   - 初始化怪兽池(从 D_CARD 按 level 切成 low / middle / high / extra)
   - 掷骰决定 shouldWin = random() < botWinRate
   - 记录 duelStartTurn

2. 决定先后手 (TITLE.decideWhoFirst):
   - shouldWin=True  → 选先手
   - shouldWin=False → 选后手

3. 每回合 onTick (己方回合自动启动 y_bot_operateRepeat):
   ┌─ 主阶段1 (y_mainPhase1)
   │     A. y_fillSmallMonsters(): 铺小怪到上限
   │        - 赢局留 1 格给招牌怪 (limit=2), 输局填满 (limit=3)
   │        - 优先用 _getPreferSmallCards()(从 preferCards 里挑 LV<=4), 否则用全局 lowlevelMonsterPool
   │     B. 娱乐期 (turnsPassed < funTurns): 直接结束, 只铺小怪不出大怪
   │     C. 赢局且 signatureOnField=False:
   │        → y_tryCheatSummonBig(): 用 createCard 凭空生成招牌怪并特召
   │
   ├─ 战斗阶段 (y_dealBattle)  [循环最多 5 轮, 不切守备]
   │     - 赢局: 每只怪都尝试攻击
   │            * 有敌方怪 → 找攻击力低于自己的打 (打不过的不打)
   │            * 无敌方怪 → 直接攻击玩家
   │     - 输局 (手下留情):
   │            * 每只怪每轮只有 losingAttackChance (默认 0.4) 概率攻击
   │            * 直攻玩家时, 玩家血量低于 losingMercyHpRatio*INIT_LP (默认 50%) 才启动留情:
   │                血越低跳过概率越高, 线性映射 (剩 50% 不跳过, 剩 0% 必跳过)
   │
   └─ y_turnEnds()

【弹窗 / 卡牌选择策略】
- y_onShowPopUp:
    * 猜拳: 随机
    * 是否发动效果: 输局一律不发动; 赢局且效果来源是招牌怪 → 必发动
    * 其他: defaultOption

- y_onShowCardSelectorPanel:
    * 输局: 能取消就取消, 否则给最低限度合法解
    * 赢局: 走 _pickByPolicy
        - title 分三类 → 不同排序方向:
            harm_enemy   (摧毁/除外/送墓/回手回库/夺控/伤害/指定): 选最强敌方威胁
            self_cost    (上贡/丢弃):                              选最弱(代价最低)
            self_benefit (加手/特召/融合/装备/变形):                选最强/最有用
        - legalGroups 优先: 整组打分后取最优组
        - 评分函数 _scoreCard:
            base = card.getCurNumber()
            招牌怪      +5000
            己方小怪    -1000 (随便弃)
            等级        ×50
            场上 +200, 手牌 +100
            敌方守备表示 ×0.7

【MENU_BOTS 配置项】
    botWinRate          : 本局赢的概率 (0.0~1.0)
    funTurns         : 娱乐期回合数, 期间只铺小怪不出大怪
    preferCards      : 卡组高频卡 cardKey 列表(LV<=4 的会被视为"专属小怪"; 重复出现即权重)
    signatureMonsters: 招牌大怪 cardKey 列表; 留空则用全局 highLevelMonsterPool

【关键状态字段】
    shouldWin         本局应赢/输
    signatureOnField  招牌大怪是否已在场 (避免反复作弊召唤)
    duelStartTurn     本局开始时的回合数 (用于计算娱乐期)
    turnWaitedAtStart 回合开始的初始等待是否已执行
================================================================================
"""
BOT_DECK1 = {

}

BATTLE_TAGS={
    "normal<4":"普通的比4弱的单位",
    "fanpan":"翻盘大怪"
}

class BotInspect:
    IS_FIRST=-1 #True False
    USED_SERIES=[]
    USED_RACES=[RACE.INSECT]
    USED_CARDS=[]



def AI_MSG(*s):
    if True:
        DEBUG_MSG(*s)


class DuelAIBase(Reload):
    avatar: AvatarCE = None
    duel:Duel=None
    game:Game
    def __init__(self, avatar):
        Reload.__init__(self,True,False)
        self.avatar = avatar

    def getSide(self):
        return self.avatar.c_side

    def getEnemySideTuple(self)->Tuple[int]:
        return self.duel.getEnemySideTuple(self.getSide())

    #get my side and ally side tuple
    def getAllySideTuple(self)->Tuple[int]:
        return self.duel.getAllySideTuple(self.getSide())


    def onDuelStart(self,duel):
        self.duel=duel
        self.game=duel.game
        #stage == rps

    def onTurnStart(self):
        pass

    #开局异步初始化(向玩家 base 请求本局赢/输等); 默认无操作
    def y_initDuelAI(self):
        yield None

    def onDuelEnd(self,duel):
        pass

    def y_signal(self,signal):
        pass


    """
    choose from popup window
    
    return option
    """
    def y_onShowPopUp(self,title:str,text:str,options:[str],defaultOption:int,canCancel:bool,popupType:POPUP_TYPE,otherSelected:Dict[int,int])->int:
        yield WaitForSeconds(0.6)

        if title==TITLE.decideWhoFirst:
            pass
        return defaultOption

    """
    choose from list of cards

    title,other title
    otherSelected:other player already selected
    
    return option,selectedCardList
    """
    def y_onShowCardSelectorPanel(self, title:TITLE,options:[str], cardList: [Card], minNum:int, maxNum:int, defaultOption:int, defaultResult: [Card], canCancel:bool, hasOrder:bool,legalGroups:[[Card]],otherSelected:Dict[int,Tuple[int,[Card],float]])->Tuple[int, [Card]]:
        if not defaultResult:
            defaultResult=[]
        yield WaitForSeconds(0.6)

        if title==TITLE.inBattleCanActivate:
            pass

        return (defaultOption,defaultResult)

    """
    these are queue of effects can be triggered,return the final queue
    """
    def y_arrangeTriggerEffects(self, queue: List[Effect])->List[Effect]:
        return queue

    def y_selectInstantEffect(self, queue: List[Effect])->Effect:
        if len(queue):
            return queue[0]
        return None


    #called every 0.3s
    def onTick(self):
        selfside=self.avatar.c_side
        duel=self.duel=self.avatar.getDuel()
        if not duel or not duel.game:
            return

        if duel.hasLoser():
            return

        if duel.stage != DUEL_STAGE.dueling:
            return

        #ai is no need in enemy's turn
        if duel.game.whoseTurn!=selfside:
            return

        duelNode=duel.duelNode
        if not duelNode.hasCoroutine("y_bot_operateRepeat"):
            duelNode.startCoroutine(self.y_bot_operateRepeat(),False,0)

    """
        main loop of bot's logic
    """
    def y_bot_operateRepeat(self):
        pass




class BOT_AI_STATE:
    stop=""
    random="random"
    smooth="smooth"
    playerMaltreat="playerMaltreat"
    strong="strong"
    overwhelming="overwhelming"


class AI_FLAG:
    summon=1


"""
used for "y_onShowPopUp" and "y_onShowCardSelectorPanel"


"""
class CHOICE_TYPE(MyEnum):
    popup=1
    selector=2

class EXPIRE(MyEnum):
    turnend=1
    nextturnend=2
    forever=3

class ChoicePredo:
    type=CHOICE_TYPE.popup
    expire=EXPIRE.turnend



USED_CARD=[]
KEY_CARD=[]


# ============================================================
# 赢局/输局池在账号侧 (AccountFunc.playerDataJ["winLose"])。
# bot AI 通过协程异步访问 (cell <-> base, #p 暴露):
#   开局: y_initDuelAI -> playerCE.base.reqDuelShouldWin(duelNode)
#         base 抽取 -> duelNode.onDuelShouldWinResult -> 解开 WaitForCB
#   终局: onDuelEnd -> playerCE.base.reportDuelOutcome(intended, botWon)
# ============================================================


class DuelAINormal(DuelAIBase):
    turnWaitedAtStart=False

    # --- 本局核心状态 ---
    shouldWin=False         # 本局应该赢还是输
    signatureOnField=False  # 招牌大怪是否已在场
    duelStartTurn=0         # 本局开始时的回合数
    cheatTurnRolled=6       # 本局开始时随机出的"招牌怪可登场"回合数

    # --- additional 难度设置 ---
    # 输局时, bot 召唤的所有攻击力 >900 的怪兽会被施加 -500 ATK 永久 buff
    ADDITIONAL_LOSE_ATK_THRESHOLD=900
    ADDITIONAL_LOSE_ATK_PENALTY=-500


    def onDuelStart(self,duel):
        DuelAIBase.onDuelStart(self, duel)
        self._initCardCount()
        self.initGeneratePool()
        self.duelStartTurn=duel.game.curTurn

        # 本局赢/输改由开局后的 y_initDuelAI 异步向玩家 base 请求决定,
        # 这里先给安全默认值(y_initDuelAI 会覆盖)
        self.shouldWin=False
        self._outcomeReported=False
        self.signatureOnField=False

        # 招牌怪登场冷却: 至少 cheatTurn 回合, 再随机 ±2 让时机不固定
        config=self.getBotConfig()
        cheatTurn=config.get("cheatTurn",6)
        self.cheatTurnRolled=max(1, cheatTurn+random.randint(-1,2))

        AI_MSG("bot duel start (shouldWin pending y_initDuelAI), cheatTurn=",
               self.cheatTurnRolled)


    # ============================================================
    # 开局异步初始化: 向玩家 base 请求本局赢/输, 等回包后设定 shouldWin
    #   由 Duel.y_startDuel -> y_initBotAIs 在 duelNode 协程里 yield 调用,
    #   所以 base 的回包要回到 duelNode (作为 callbacker 传过去)。
    # ============================================================
    def y_initDuelAI(self):
        config=self.getBotConfig()
        botWinRate=config.get("botWinRate",0.5)
        sw=None
        playerCE=self._getOutcomePlayerCE()
        if playerCE is not None and getattr(playerCE,"base",None):
            # base 抽取后回调 duelNode.onDuelShouldWinResult -> 解开下面的 WaitForCB
            playerCE.base.reqDuelShouldWin(self.duel.duelNode)
            waitResult=yield WaitForCB("onDuelShouldWinResult",5)
            if waitResult.called and waitResult.args:
                sw=bool(waitResult.args[0])
        if sw is None:
            sw=random.random()<botWinRate    # 无真人玩家/超时兜底
        self.shouldWin=bool(sw)
        self._outcomeReported=False
        AI_MSG("y_initDuelAI shouldWin=",self.shouldWin)


    def getBotName(self):
        """本局使用的 MENU_BOTS key (由 Duel._botName 指定)"""
        try:
            return self.duel._botName
        except Exception:
            return None

    def getBotConfig(self):
        """获取 MENU_BOTS 中对应本 bot 的配置,子类可覆盖"""
        botName=self.getBotName()
        if botName and botName in MENU_BOTS:
            return MENU_BOTS[botName]
        # 兜底: 旧逻辑, 按 aiClass 匹配第一个
        for key,cfg in MENU_BOTS.items():
            if cfg.get("aiClass")==self.__class__ or cfg.get("aiClass")==DuelAINormal:
                return cfg
        return {}


    # ============================================================
    # 终局: 对比预定结果与实际胜负, 不符则把预定结果塞回池里补偿
    # ============================================================
    def _getOutcomePlayerCE(self):
        """取人类玩家的 AvatarCE(持久池在其 base/账号侧); 无则 None(bot对bot/测试)"""
        try:
            return self.duel.getNotBotAvatar(self.getEnemySideTuple()[0])
        except Exception:
            return None

    def onDuelEnd(self, duel):
        if getattr(self, "_outcomeReported", False):
            return
        self._outcomeReported=True

        try:
            losers=duel._losers or {}
        except Exception:
            return
        if not losers:
            return

        botLost=self.getSide() in losers
        # 平局(双方都输)不补偿
        if len(losers)>=2 and botLost:
            AI_MSG("[outcome] draw, skip")
            return

        # 终局 -> 玩家 base 做补偿+持久化 (cell->base, 无需回包)
        playerCE=self._getOutcomePlayerCE()
        if playerCE is not None and getattr(playerCE,"base",None):
            playerCE.base.reportDuelOutcome(self.shouldWin, not botLost)


    # ============================================================
    # 怪兽池初始化 (从 D_CARD 分级)
    # ============================================================
    lowlevelMonsterPool:List[str]=None     # LV<=4 小怪池(config + D_CARD 补足, >=10 unique)
    middleLevelMonsterPool:List[str]=None  # LV5-6 中级怪池
    highLevelMonsterPool:List[str]=None    # LV>=7 大怪池
    signatureMonstersPool:List[str]=None   # 招牌怪池(config 优先, 不限等级)
    extraMonsterPool:List[str]=None        # 额外怪(融合/同调等 whiteMonster)
    POOL_MIN_UNIQUE=10                     # 每个池子至少要的 unique cardKey 数
    CARD_CREATE_LIMIT=3                    # 每种 cardKey 凭空 createCard 的总数硬上限
    SIG_LOW_PICK_CHANCE=0.3                # 铺低级怪时, 从 signatureMonstersPool 抽 LV<=4 的概率
    cardCreatedCount=None                  # {cardKey: 当前已存在/已被 createCard 的张数}

    # ============================================================
    # createCard 计数表: 防止凭空 createCard 让同名卡超过 3 张
    # ============================================================
    def _initCardCount(self):
        """开局: 把 config['deck'] 里每张卡的数量灌入计数表"""
        self.cardCreatedCount={}
        config=self.getBotConfig()
        deck=config.get("deck") or {}
        if isinstance(deck, dict):
            for groupKey, cardList in deck.items():
                if not isinstance(cardList, (list, tuple)):
                    continue
                for cardKey in cardList:
                    self.cardCreatedCount[cardKey]=self.cardCreatedCount.get(cardKey,0)+1
        elif isinstance(deck, (list, tuple)):
            for cardKey in deck:
                self.cardCreatedCount[cardKey]=self.cardCreatedCount.get(cardKey,0)+1

    def _canCreateMore(self, cardKey)->bool:
        """这张卡是否还能再 createCard 一张(< CARD_CREATE_LIMIT)"""
        if self.cardCreatedCount is None:
            return True
        return self.cardCreatedCount.get(cardKey,0)<self.CARD_CREATE_LIMIT

    def _onCreateCard(self, cardKey):
        """成功 createCard 后调用, 计数 +1"""
        if self.cardCreatedCount is None:
            self.cardCreatedCount={}
        self.cardCreatedCount[cardKey]=self.cardCreatedCount.get(cardKey,0)+1

    def _pickCreatableFromPool(self, pool):
        """从 pool 里随机挑一张还能 createCard 的 cardKey; 全部超限返回 None"""
        if not pool:
            return None
        candidates=[k for k in pool if self._canCreateMore(k)]
        if not candidates:
            return None
        return random.choice(candidates)

    def _isLowLevel(self, cardKey):
        j=D_CARD.get(cardKey)
        if not j:
            return False
        lv=j.get("level",0)
        return 1<=lv<=4

    def _pickLowLevelMonsterKey(self):
        """挑一张可以 createCard 的低等级怪兽 cardKey
           1) 按 SIG_LOW_PICK_CHANCE 概率从 signatureMonstersPool 内的 LV<=4 部分挑
           2) 否则从 lowlevelMonsterPool 挑
        """
        if random.random()<self.SIG_LOW_PICK_CHANCE:
            sigLow=[k for k in (self.signatureMonstersPool or [])
                    if self._isLowLevel(k) and self._canCreateMore(k)]
            if sigLow:
                return random.choice(sigLow)
        return self._pickCreatableFromPool(self.lowlevelMonsterPool)


    def initGeneratePool(self):
        """开局构建 4 个怪兽池: low/middle/high/signature
           1) 先从 config['preferCards'] / config['signatureMonsters'] 抽取
           2) 不足 POOL_MIN_UNIQUE 种时, 从 D_CARD 随机补足, 优先匹配 config['preferRace']
        """
        config=self.getBotConfig()
        preferCards=config.get("preferCards") or []
        sigCards=config.get("signatureMonsters") or []
        preferRace=config.get("preferRace")    # 可以是单个 RACE 或 list/tuple/set

        # --- 配置优先 + 等级分桶 ---
        self.lowlevelMonsterPool   = self._filterCfgCards(preferCards, 1, 4)
        self.middleLevelMonsterPool= self._filterCfgCards(preferCards, 5, 6)
        self.highLevelMonsterPool  = self._filterCfgCards(preferCards, 7, 999)
        self.signatureMonstersPool = self._filterCfgCards(sigCards,    1, 999)

        # --- 额外怪兽池(融合/同调等)按 D_CARD 全扫一遍即可 ---
        self.extraMonsterPool=[]
        for cardKey, j in D_CARD.items():
            if cardKey=="version":
                continue
            try:
                t=cardTypeStrToInt(j["type"], cardKey)
            except Exception:
                continue
            if (t & CARD_TYPE.monster) and (t & CARD_TYPE.whiteMonster)==CARD_TYPE.whiteMonster:
                self.extraMonsterPool.append(cardKey)

        # --- 不足 POOL_MIN_UNIQUE 时补足 ---
        self._supplementPool(self.lowlevelMonsterPool,    1, 4,   preferRace)
        self._supplementPool(self.middleLevelMonsterPool, 5, 6,   preferRace)
        self._supplementPool(self.highLevelMonsterPool,   7, 999, preferRace)
        # 招牌怪池补足时仍走"高等级"语义
        self._supplementPool(self.signatureMonstersPool,  7, 999, preferRace)

        self.printPools()


    def _filterCfgCards(self, keyList, lvMin=1, lvMax=999):
        """从 cardKey 列表里过滤出合法的怪兽 cardKey, 保留重复以保权重"""
        result=[]
        for cardKey in keyList:
            j=D_CARD.get(cardKey)
            if not j:
                continue
            try:
                t=cardTypeStrToInt(j["type"], cardKey)
            except Exception:
                continue
            if not (t & CARD_TYPE.monster):
                continue
            # 额外怪不进 main 池
            if (t & CARD_TYPE.whiteMonster)==CARD_TYPE.whiteMonster:
                continue
            lv=j.get("level", 0)
            if lv<lvMin or lv>lvMax:
                continue
            result.append(cardKey)
        return result


    def _supplementPool(self, pool, lvMin, lvMax, preferRace):
        """如 pool 内 unique cardKey < POOL_MIN_UNIQUE, 从 D_CARD 随机抽合规怪兽补足"""
        unique=set(pool)
        need=self.POOL_MIN_UNIQUE-len(unique)
        if need<=0:
            return

        def _collect(useRace):
            out=[]
            for cardKey, j in D_CARD.items():
                if cardKey=="version" or cardKey in unique:
                    continue
                try:
                    t=cardTypeStrToInt(j["type"], cardKey)
                except Exception:
                    continue
                if not (t & CARD_TYPE.monster):
                    continue
                if (t & CARD_TYPE.whiteMonster)==CARD_TYPE.whiteMonster:
                    continue
                lv=j.get("level", 0)
                if lv<lvMin or lv>lvMax:
                    continue
                if useRace and preferRace:
                    try:
                        r=cardRaceStrToInt(j["race"], cardKey)
                    except Exception:
                        continue
                    if isinstance(preferRace, (list, tuple, set)):
                        if r not in preferRace:
                            continue
                    else:
                        if r!=preferRace:
                            continue
                out.append(cardKey)
            return out

        # 先尝试 preferRace 过滤后的候选
        candidates=_collect(useRace=True)
        random.shuffle(candidates)
        for ck in candidates:
            if need<=0: break
            pool.append(ck); unique.add(ck); need-=1

        # 仍不够 -> 放宽种族限制再补
        if need>0 and preferRace:
            candidates=_collect(useRace=False)
            random.shuffle(candidates)
            for ck in candidates:
                if need<=0: break
                pool.append(ck); unique.add(ck); need-=1


    def printPools(self):
        """打印 4 个怪兽池的内容(开局时自动调用一次)"""
        def _fmt(pool):
            counter={}
            for k in pool:
                counter[k]=counter.get(k,0)+1
            items=", ".join((k+"x"+str(v)) if v>1 else k for k,v in counter.items())
            return "total=%d unique=%d [%s]" % (len(pool), len(counter), items)
        AI_MSG("[pool] lowlevelMonsterPool    :", _fmt(self.lowlevelMonsterPool or []))
        AI_MSG("[pool] middleLevelMonsterPool :", _fmt(self.middleLevelMonsterPool or []))
        AI_MSG("[pool] highLevelMonsterPool   :", _fmt(self.highLevelMonsterPool or []))
        AI_MSG("[pool] signatureMonstersPool  :", _fmt(self.signatureMonstersPool or []))

    def onTurnStart(self):
        self.turnWaitedAtStart=False

    def y_signal(self,signal):
        pass


    # ============================================================
    # 弹窗 / 卡牌选择面板
    # ============================================================

    # ---- title 分类表: 决定排序方向 ----
    # "harm_enemy"   : 害敌(选最强威胁)
    # "self_cost"    : 自损/代价(选最弱)
    # "self_benefit" : 收益(选最强/最有用)
    _HARM_ENEMY_TITLES = {
        TITLE.destroy, TITLE.banish, TITLE.sendToGrave,
        TITLE.returnToHand, TITLE.returnToDeck,
        TITLE.changeController, TITLE.damage, TITLE.target,
    }
    _SELF_COST_TITLES = {
        TITLE.tribute, TITLE.discard,
    }
    _SELF_BENEFIT_TITLES = {
        TITLE.addToHand, TITLE.specialSummon, TITLE.fusionSummon,
        TITLE.equip, TITLE.changeForm,
    }


    def _classifyTitle(self, title) -> str:
        if title in self._HARM_ENEMY_TITLES:
            return "harm_enemy"
        if title in self._SELF_COST_TITLES:
            return "self_cost"
        if title in self._SELF_BENEFIT_TITLES:
            return "self_benefit"
        return "neutral"


    def _scoreCard(self, card: Card, friendly: bool) -> float:
        """对一张卡打分。friendly=True 表示该卡属于自己阵营。
        分数越高 = 越值钱(自己留着越好,或敌方威胁越大)。"""
        if card is None:
            return 0
        config = self.getBotConfig()
        sig = self.signatureMonstersPool or []
        small = self.lowlevelMonsterPool or []

        try:
            base = float(card.getCurNumber())
        except Exception:
            base = 0.0

        # 招牌怪极高权重: 自己 = 宝贝, 敌方 = 必须解
        if card.cardKey in sig:
            base += 5000

        # 小怪在己方几乎无价值, 可随便献祭/弃
        if friendly and card.cardKey in small:
            base -= 1000

        # 等级权重: 高级怪在手 / 牌堆里更值得搜
        base += getattr(card, "level", 0) * 50

        # 位置加成
        try:
            if card.isOnField():
                base += 200
            elif card.isInHand():
                base += 100
        except Exception:
            pass

        # 敌方守备表示威胁打折
        try:
            if not friendly and card.isDefence():
                base *= 0.7
        except Exception:
            pass

        return base


    def _pickByPolicy(self, title, cardList, minNum, maxNum, legalGroups):
        """核心选择策略, 返回选好的卡牌列表。"""
        mySide = self.getSide()
        enemySides = self.getEnemySideTuple()
        policy = self._classifyTitle(title)

        # --- 1. 有 legalGroups: 先按组打分, 再返回最优组 ---
        if legalGroups:
            def groupScore(g):
                total = sum(self._scoreCard(c, c.side == mySide) for c in g)
                if policy == "self_cost":
                    return -total          # 代价: 总价值越低越好
                return total               # 害敌/收益: 总价值越高越好
            best = max(legalGroups, key=groupScore)
            picked = list(best)
            if maxNum and len(picked) > maxNum:
                picked = picked[:maxNum]
            return picked

        if not cardList:
            return []

        # --- 2. 普通: 按 policy 排序后切片 ---
        def sortKey(c):
            friendly = (c.side == mySide)
            s = self._scoreCard(c, friendly)
            if policy == "self_cost":
                return s                    # 升序: 选最弱
            if policy == "harm_enemy":
                # 优先打敌方, 威胁越大越优先
                bias = 10000 if c.side in enemySides else 0
                return -(s + bias)
            if policy == "self_benefit":
                bias = 10000 if friendly else 0
                return -(s + bias)
            return -s                       # neutral: 价值高的优先

        ordered = sorted(cardList, key=sortKey)

        # 收益 / 害敌类尽量多选(到 maxNum); 代价类只够 minNum
        if policy in ("self_benefit", "harm_enemy"):
            n = max(minNum, min(maxNum, len(ordered)))
        else:
            n = max(minNum, 1)
            n = min(n, maxNum if maxNum else n, len(ordered))
        return ordered[:n]


    def y_onShowPopUp(self, title, text, options, defaultOption,
                      canCancel, popupType:POPUP_TYPE, reasonCard):
        yield WaitForSeconds(0.6)

        # 猜拳: 随机
        if popupType == POPUP_TYPE.rockpaperscissors:
            return random.randint(0, 2)

        # 决定先后手: 赢局先手, 输局后手
        if title == TITLE.decideWhoFirst:
            return 0 if self.shouldWin else 1

        # 是否发动效果
        if title == TITLE.shouldActivate:
            if not self.shouldWin:
                return 1                                    # 输局: 不发动
            sig = self.signatureMonstersPool or []
            if reasonCard is not None and getattr(reasonCard, "cardKey", "") in sig:
                return 0                                    # 招牌怪效果一定发动
            return defaultOption

        # 长文本(连锁选择): 走默认
        try:
            if popupType == POPUP_TYPE.longText:
                return defaultOption
        except Exception:
            pass

        # 通用 YES/NO / askbattle: 顺势返回默认(战斗策略由 y_dealBattle 控)
        return defaultOption


    def y_onShowCardSelectorPanel(self, title:str, options:[str], cardList:[Card],
                                  minNum=1, maxNum=1,
                                  defaultOption:int=0, defaultResult:[Card]=DEFAULT_RESULT.random,
                                  canCancel=False, hasOrder=False,
                                  legalGroups:[[Card]]=None,
                                  otherSelected:Dict[int,Tuple[int,[Card],float]]=None
                                  ) -> Tuple[int, [Card]]:
        yield WaitForSeconds(0.6)

        # 没东西可选
        if not cardList and not legalGroups:
            return (defaultOption, [])

        # ---- 输局: 能取消就取消, 否则给一个最低限度的合法解 ----
        if not self.shouldWin:
            if canCancel:
                return (1, [])                              # 1 = CANCEL
            if isinstance(defaultResult, list) and defaultResult:
                return (defaultOption, defaultResult)
            fallback = (cardList[:max(minNum, 1)] if cardList else [])
            return (defaultOption, fallback)

        # ---- 赢局: 走策略 ----
        picked = self._pickByPolicy(title, cardList, minNum, maxNum, legalGroups)

        # 兜底: 满足 minNum
        if len(picked) < minNum and cardList:
            rest = [c for c in cardList if c not in picked]
            picked = list(picked) + rest[:(minNum - len(picked))]

        AI_MSG("pickPolicy", title, "->", [getattr(c, "cardKey", "?") for c in picked])
        return (defaultOption, picked)


    # ============================================================
    # 主循环
    # ============================================================
    def y_bot_operateRepeat(self):
        game=self.game
        side=self.getSide()

        INFO_MSG("start bot ai, turn=",game.curTurn)
        if not self.turnWaitedAtStart:
            self.turnWaitedAtStart=True
            yield WaitForSeconds(2)

        # --- 主阶段1: 铺场 ---
        yield self.y_mainPhase1()

        # --- 不战斗: 跳过所有等待, 立刻结束回合 ---
        if not self._willAttackThisTurn():
            yield game.y_turnEnds()
            return

        yield WaitForSeconds(random.uniform(2,3))

        # --- 战斗阶段 ---
        yield self.y_dealBattle()

        yield WaitForSeconds(1)
        yield game.y_turnEnds()


    # ============================================================
    # 主阶段1: 优先打手牌, 再铺小怪, 视情况出大怪
    # ============================================================
    def y_mainPhase1(self):
        game=self.game
        side=self.getSide()
        config=self.getBotConfig()
        turnsPassed=game.curTurn-self.duelStartTurn
        funTurns=config.get("funTurns",3)

        # A0. 优先用手牌里的 LV<=4 怪进行通常召唤
        yield self.y_summonFromHand()

        # A. 然后铺小怪给玩家打
        yield self.y_fillSmallMonsters()

        # B. 娱乐期内(前 funTurns 回合): 只铺小怪, 不做其他事
        if turnsPassed<funTurns:
            return

        # C. 赢局 + 已过招牌怪冷却回合 + 招牌怪未出场: 尝试召唤大怪
        if (self.shouldWin
                and not self.signatureOnField
                and turnsPassed>=self.cheatTurnRolled):
            yield self.y_tryCheatSummonBig()


    # ============================================================
    # additional 难度: 输局时对刚召唤的怪兽施加 -500 ATK 永久 buff (ATK>900 才触发)
    # ============================================================
    def y_applyAdditionalLosingDebuff(self, monster:Card):
        """输局 additional 难度: 若 monster 当前攻击力 > 900, 施加 -500 ATK 永久 buff"""
        try:
            curAtk = monster.getCurNumber()
        except Exception:
            curAtk = getattr(monster, "atk", 0)
        if curAtk <= self.ADDITIONAL_LOSE_ATK_THRESHOLD:
            return
        yield self.game.y_addCardData(monster,attackAdd=-500,fx=FX_ID.notExist)
        AI_MSG("additional losing debuff applied:", getattr(monster, "cardKey", "?"),
               "atk", curAtk, "->", curAtk + self.ADDITIONAL_LOSE_ATK_PENALTY)

    # ============================================================
    # 手牌召唤: 从 hand 中找 LV<=4 怪兽进行通常召唤(消耗本回合 normalSummon 次数)
    # 优先级: 招牌怪 > preferCards 中的 LV<=4 怪 > 攻击力高的
    # ============================================================
    def y_summonFromHand(self):
        game=self.game
        side=self.getSide()
        config=self.getBotConfig()

        # 没有 normalSummon 次数 / 没空位 -> 不召
        if game.normalSummonCntThisTurn[side]>=game.normalSummonCntLimit[side]:
            return
        if game.freeMonsterSpace(side)<=0:
            return

        # 手牌里 LV<=4 的怪(无需祭品)
        handMonsters=[c for c in game.hands[side]
                      if (c.cardType & CARD_TYPE.monster) and c.level<=4 and c.level>0 and game.checkCanNormalSummon(c)
                      ]
        if not handMonsters:
            return

        sig=self.signatureMonstersPool or []
        small=self.lowlevelMonsterPool or []
        def score(c):
            s=c.getCurNumber()
            if c.cardKey in sig:   s+=5000
            if c.cardKey in small: s+=200
            return s
        handMonsters.sort(key=score, reverse=True)

        target=handMonsters[0]
        ok=yield game.y_normalSummon(False, target)
        if ok:
            AI_MSG("normal summon from hand:", target.cardKey)
            yield self.y_applyAdditionalLosingDebuff(target)
            yield WaitForSeconds(2)


    # ============================================================
    # 铺小怪: 核心娱乐机制
    # 优先使用 preferCards 里 LV<=4 的怪, 没有则用全局 lowlevelMonsterPool
    # ============================================================
    def y_fillSmallMonsters(self):
        game=self.game
        side=self.getSide()
        config=self.getBotConfig()

        # 赢局给大怪留1个格子, 输局尽量填满
        limit=2 if (self.shouldWin and not self.signatureOnField) else 3
        monsters=game.monsters[side]

        while len(monsters)<limit:
            # 优先用 config 中配置的专属小怪
            monsterKey=self._pickLowLevelMonsterKey()
            if not monsterKey:
                break  # 低级池/招牌池里候选都达 3 张上限

            monster=game.createCard(monsterKey,side)
            self._onCreateCard(monsterKey)
            ok=yield game.y_normalSummon(False,monster,costNormalSummonChance=False)
            if not ok:
                break
            yield self.y_applyAdditionalLosingDebuff(monster)
            yield WaitForSeconds(2)


    # ============================================================
    # 作弊召唤大怪
    # 赢局 + 娱乐期结束 + 招牌怪未出场时调用
    # 直接用 createCard 凭空创建招牌大怪并特殊召唤
    # ============================================================
    def y_tryCheatSummonBig(self):
        game=self.game
        side=self.getSide()
        config=self.getBotConfig()

        monsterKey=self._pickCreatableFromPool(self.signatureMonstersPool)
        if not monsterKey:
            return  # 没招牌怪 / 全部已达 3 张上限

        monster=game.createCard(monsterKey,side)
        self._onCreateCard(monsterKey)
        ok=yield game.y_specialSummon(monster)
        if ok:
            self.signatureOnField=True
            AI_MSG("cheat summon big monster:",monsterKey)
            yield self.y_applyAdditionalLosingDebuff(monster)


    # ============================================================
    # 战斗阶段
    # shouldWin=True:  主动攻击, 先打弱的敌怪, 没敌怪则直接攻击
    # shouldWin=False: 手下留情 — 降低攻击频率, 玩家血量低时概率不直攻玩家
    # ============================================================
    losingAttackChance=0.4    # 输局: 每只怪每轮的攻击概率
    losingMercyHpRatio=0.5    # 输局: 玩家剩余血量低于该比例(占 INIT_LP)时, 启动直攻概率跳过

    def _canAttackFilter(self, card):
        if card.form!=FORM.attack:
            return False
        if not card.checkBuffCanAttack():
            return False
        if card.attackCntThisTurn>=card.attackCntLimitPerTurn:
            return False
        return True

    def _willAttackThisTurn(self):
        """预判本回合是否会真正发起攻击; 否则不切换战斗阶段, 直接 endturn"""
        game=self.game
        side=self.getSide()

        attackers=game.searchCards(LOCATION.monsterZone, side, CARD_TYPE.monster,
                                   filterFunc=self._canAttackFilter)
        if not attackers:
            return False

        enemyMonsters=game.searchCards(LOCATION.monsterZone, self.getEnemySideTuple(),
                                       CARD_TYPE.monster)
        if enemyMonsters:
            # 有敌方怪: 至少要有一只我方攻击力 > 某只敌方怪, 才会真的打
            weakest=min(em.getCurNumber() for em in enemyMonsters)
            return any(m.getCurNumber()>weakest for m in attackers)

        # 没有敌方怪兽 = 可以直攻; 输局的手下留情概率即使会跳过, 这里保守返回 True
        return True

    def y_dealBattle(self):
        game=self.game
        side=self.getSide()

        # --- 不准备攻击 -> 不切换战斗阶段, 直接结束 ---
        if not self._willAttackThisTurn():
            return

        if game.phase==PHASE.mainphase1:
            yield game.y_changePhase()
        if game.phase!=PHASE.battle:
            return

        canAttackFilter=self._canAttackFilter

        for i in range(5):
            myCanAttackMonsters=game.searchCards(LOCATION.monsterZone,side,CARD_TYPE.monster,filterFunc=canAttackFilter)
            if not len(myCanAttackMonsters):
                break

            random.shuffle(myCanAttackMonsters)
            progressed=False

            for monster in myCanAttackMonsters:
                # 能攻击就攻击 (输局也照常出手, 只在"会致死"时收手, 见下)
                enemyMonsters=game.searchCards(LOCATION.monsterZone,self.getEnemySideTuple(),CARD_TYPE.monster)

                if len(enemyMonsters)>0:
                    # 找攻击力比自己低的敌怪打
                    random.shuffle(enemyMonsters)
                    for enemyMonster in enemyMonsters:
                        if enemyMonster.getCurNumber()<monster.getCurNumber():
                            yield game.y_player_monsterAttack(monster,enemyMonster)
                            yield WaitForSeconds(3)
                            progressed=True
                            break
                else:
                    # 没有敌方怪兽: 直攻玩家
                    # 输局 bot 也照常打, 不作弊也不手下留情(能打死就打死),
                    # 胜负偏差交给全局赢局/输局池补偿
                    targetSide=random.choice(self.getEnemySideTuple())
                    yield game.y_player_monsterAttack(monster,targetSide)
                    yield WaitForSeconds(3)
                    progressed=True

            # 没有任何攻击发生(都被概率跳过 / 都打不过), 提前结束避免空转
            if not progressed:
                break



"""
子类示例: 龙族 AI (可覆盖 getBotConfig 指向特定配置)
"""
class DuelAI_dragon(DuelAINormal):
    pass




MENU_BOTS={
    TESTPLAY_BOT:{
        "avatarKey":"yblack",
        "picture":"",
        "title":"",
        "description":"",
        "aiClass":DuelAINormal,
        "deck":decks.DEBUG_DECK1,
        "preferScene":DEBUG_SCENE,
        # --- AI 新配置 ---
        "botWinRate":0.2,              # 赢的概率
        "funTurns":3,               # 娱乐期回合数(只铺小怪)
        "signatureMonsters":[],     # 留空则用全局 highLevelMonsterPool
    },
    "tutorialBot":{
        "avatarKey":"yblack",
        "picture":"",
        "title":"",
        "description":"",
        "aiClass":DuelAINormal,
        "deck":decks.DEBUG_DECK1,
        "preferScene":"cc/factory_parking/factory_parking",
        "botWinRate":0.2,              # 教程bot必输
        "funTurns":99,              # 永远只铺小怪
        "signatureMonsters":[],
    },
    "bot1":{
        "avatarKey":"yblack",
        "picture":"Clash for Supremacy",
        "title":"Clash for Supremacy",
        "description":"",
        "aiClass":DuelAINormal,
        "deck":decks.DEBUG_DECK1,
        "preferRace":RACE.DRAGON,
        "preferCards":[
            "ToonDragon_Lowpoly","cartoonDragon","cartoonLeviathan","cartoonWyvern",
            "SK_BabyDragon","Dragon Inferno","FireDragonRed","ForestDrake_Blue",
            "smallDragonWhelp_Rd","Fantasy Dragon-Blue","Drake Skinny",
        ],
        "preferScene":"cc/factory_parking/factory_parking",
        "botWinRate":0.2,
        "funTurns":3,
        "signatureMonsters":[
            "MountainDragon","cartoonChineseDragon","Wyrm1_2","Wyvern","dragonrex",
        ],
    },
    "bot2":{
        "avatarKey":"greentrenchcoatman",
        "picture":"Abyssal Sea Hunting Grounds",
        "title":"Abyssal Sea Hunting Grounds",
        "description":"",
        "aiClass":DuelAINormal,
        "deck":decks.DEBUG_DECK1,
        "preferRace":RACE.AQUA,
        "preferCards":[
            "Bass_LOD0","CrabMonsterDefault","Catfish_LOD0","giantcrab",
            "weranglerfish","SKM_whale","Walrus_LOD0","SeaLion_LOD0","StoneBeast",
        ],
        "preferScene":"cc/modular_town/modular_town",
        "botWinRate":0.2,
        "funTurns":3,
        "signatureMonsters":[
            "werecrab","Voidray","toon_Lobster","SKM_squid","Turtle_Blue_Shell_01",
        ],
    },
    "bot3":{
        "avatarKey":"greentrenchcoatman",
        "picture":"Carapace Vanguard",
        "title":"Carapace Vanguard",
        "description":"",
        "aiClass":DuelAINormal,
        "deck":decks.DEBUG_DECK1,
        "preferRace":RACE.INSECT,
        "preferCards":[
            "ms03_Bee_1","Wasp_Blue","Caterpillar","JapaneseHornet",
            "Ladybug","Mantis","Moth","Beast_1",
        ],
        "preferScene":"cc/modular_town/modular_town",
        "botWinRate":0.2,
        "funTurns":3,
        "signatureMonsters":[
            "GiantBeetle","RhinocerosBeetle",
        ],
    },
    "bot4":{
        "avatarKey":"whitehairman",
        "picture":"Claw of the Verdant Wilds",
        "title":"Claw of the Verdant Wilds",
        "description":"",
        "aiClass":DuelAINormal,
        "deck":decks.DEBUG_DECK1,
        "preferRace":RACE.PLANT,
        "preferCards":[
            "StumpEnt_Autumn","Sun Blossom","Spore","ms02_Stump_1",
            "Cactus Boss","Sunflower Fairy","Ent","Treant_Summer",
            "Plant Chewer","TreantGuard-Green",
        ],
        "preferScene":"cc/modular_town/modular_town",
        "botWinRate":0.2,
        "funTurns":3,
        "signatureMonsters":[
            "Sunflora Pixie",
        ],
    },
    "bot5":{
        "avatarKey":"glassredcoat",
        "picture":"Crimson Flame Tide",
        "title":"Crimson Flame Tide",
        "description":"",
        "aiClass":DuelAINormal,
        "deck":decks.DEBUG_DECK1,
        "preferRace":RACE.DRAGON,
        "preferCards":[
            "ToonDragon_Lowpoly","cartoonDragon","cartoonLeviathan","cartoonWyvern",
            "SK_BabyDragon","Dragon Inferno","FireDragonRed","ForestDrake_Blue",
            "smallDragonWhelp_Rd","Fantasy Dragon-Blue","Drake Skinny",
        ],
        "preferScene":"cc/modular_town/modular_town",
        "botWinRate":0.2,
        "funTurns":3,
        "signatureMonsters":[
            "desertdragon","Wyrm1_2","plainsdragon","polardragon","dragonrex",
        ],
    },
    "bot6":{
        "avatarKey":"brownvest",
        "picture":"Forest Little Rascal",
        "title":"Forest Little Rascal",
        "description":"",
        "aiClass":DuelAINormal,
        "deck":decks.DEBUG_DECK1,
        "preferRace":RACE.BEASTWARRIOR,
        "preferCards":[
            "OrcPBR","ms06_Rat_1","ms04_01_Minotaur_2","RatAssassinDefault",
            "WerewolfMaskTint","Kitsune_2","Dragonide",
        ],
        "preferScene":"cc/modular_town/modular_town",
        "botWinRate":0.2,
        "funTurns":3,
        "signatureMonsters":[
            "Dog Bowwow","SwordsTiger",
        ],
    },
    "bot7":{
        "avatarKey":"whitetail",
        "picture":"Growth Element",
        "title":"Growth Element",
        "description":"",
        "aiClass":DuelAINormal,
        "deck":decks.DEBUG_DECK1,
        "preferRace":RACE.FAIRY,
        "preferCards":[
            "Whirlwind","tinyWind","Lyme",
        ],
        "preferScene":"cc/modular_town/modular_town",
        "botWinRate":0.2,
        "funTurns":3,
        "signatureMonsters":[
            "Wind Mage","cartoonKitsune",
        ],
    },
    "bot8":{
        "avatarKey":"Tangsuithoodieman",
        "picture":"Jurassic Rallying Call",
        "title":"Jurassic Rallying Call",
        "description":"",
        "aiClass":DuelAINormal,
        "deck":decks.DEBUG_DECK1,
        "preferRace":RACE.DINOSAUR,
        "preferCards":[
            "Pterodactyl","Mosasaurus","Triceratops","Ankylosaurus",
            "Pachycephalosaurus","Stegosaurus","T Rex","Brachiosaurus",
            "Dilophosaurus","Parasaurolophus",
        ],
        "preferScene":"cc/modular_town/modular_town",
        "botWinRate":0.2,
        "funTurns":3,
        "signatureMonsters":[],  # disable=9åæ é«çº§æé¾æ
    },
    "bot9":{
        "avatarKey":"bwmaidoutfit",
        "picture":"Woodland Cuties",
        "title":"Woodland Cuties",
        "description":"",
        "aiClass":DuelAINormal,
        "deck":decks.DEBUG_DECK1,
        "preferRace":RACE.BEAST,
        "preferCards":[
            "Dino_Cat_04","Cat Bolt","Cat Lightning","cartoonPegasus","Goat_LOD0",
            "Werewolf","Dog Bark","ThreeTailedWolf","toon_RedPanda",
            "toon_SnappingTurtle","Lynx_LOD0","Llama_LOD0",
        ],
        "preferScene":"cc/modular_town/modular_town",
        "botWinRate":0.2,
        "funTurns":3,
        "signatureMonsters":[
            "toon_Crocodile","toon_Hedgehog","toon_Skunk","Moose_LOD0",
            "Unicorn_Pegasus","cartoonCerberus","cartoonKirin","GhostTiger",
        ],
    },
}
