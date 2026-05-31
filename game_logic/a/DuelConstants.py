# -*- coding: utf-8 -*-

class MyEnum:
    def __new__(cls, *args, **kwargs):
        import KBEDebug
        KBEDebug.ERROR_MSG("new Enum is forbidden")
    if 0:
        def __and__(self, other):
            pass





class EFF_TAG(MyEnum):
    specialSummon="specialSummon"
    destroyMonster="destroyMonster"
    destroySpellTrap="destroySpellTrap"
    retrieve="retrieve"

    ____________AI_TAGS="the following tags are used by AI"
    ai_highcost="ai_highcost"
    ai_dontuse="ai_dontuse"


# class SIGNAL(MyEnum):
#     DealtDmg="DealtDmg"
#     MonsterGetsFrozen="MonsterGetsFrozen"
#     AbilityDmg="AbilityDmg"
#     AllCured="AllCured"
#     MonstersCured="MonstersCured"
#     MonsterStatCheck="MonsterStatCheck"
#     HeroChangedHealthinTurn="HeroChangedHealthinTurn"
#     GotHealed="GotHealed"
#     MonsterAppears="MonsterAppears"
#     MonsterDisappears="MonsterDisappears"
#     MonsterChargeChanged="MonsterChargeChanged"
#     MonsterLosesDivineShield="MonsterLosesDivineShield"
#     FinalDmgonMonster="FinalDmgonMonster"
#     MonsterTakesDmg="MonsterTakesDmg"
#     MonsterTookDamage="MonsterTookDamage"
#     MonsterTakes0Dmg="MonsterTakes0Dmg"
#     MonsterTook0Dmg="MonsterTook0Dmg"
#     # MonsterDies
#     # MonsterDied
#     # MonsterPlayed
#     # MonsterSummoned
#     # MonsterBeenSummoned
#     # BattlecryTargetDecision
#     # MonsterBuffed
#     # SpellBeenCast
#     # SpellPlayed
#     # Spellboost
#     # SpellTargetDecision
#     # SpellBeenCast
#     # HeroTakesDmg
#     # Necromancy
#     # Reanimate
#     # DmgTaker
#     # TurnEnds
#     # TurnStarts
#     # BattleStarted
#     # BattleFinished
#     # SpellOKtoCast
#     # SpellBeenPlayed
#     # DeckCheck
#     # CardDrawn
#     # SpellCastWhenDrawn
#     # CardEntersHand
#     # PutinHandbyDiscover
#     # CardShuffled
#     # BurialRite
#     # CardDiscarded
#     # HandDiscarded
#     # CardLeavesHand
#     # ManaPaid
#     # CardEntersHand
#     # SecretRevealed
#
#     normalSummon="normalSummon"
#     battleEnd="battleEnd"



#define REASON_DESTROY		0x1		//
#define REASON_RELEASE		0x2		//
#define REASON_TEMPORARY	0x4		//
#define REASON_MATERIAL		0x8		//
#define REASON_SUMMON		0x10	//
#define REASON_BATTLE		0x20	//
#define REASON_EFFECT		0x40	//
#define REASON_COST			0x80	//
#define REASON_ADJUST		0x100	//
#define REASON_LOST_TARGET	0x200	//
#define REASON_RULE			0x400	//
#define REASON_SPSUMMON		0x800	//
#define REASON_DISSUMMON	0x1000	//
#define REASON_FLIP			0x2000	//
#define REASON_DISCARD		0x4000	//
#define REASON_RDAMAGE		0x8000	//
#define REASON_RRECOVER		0x10000	//
#define REASON_RETURN		0x20000	//
#define REASON_FUSION		0x40000	//
#define REASON_SYNCHRO		0x80000	//
#define REASON_RITUAL		0x100000	//
#define REASON_XYZ			0x200000	//
#define REASON_REPLACE		0x1000000	//
#define REASON_DRAW			0x2000000	//
#define REASON_REDIRECT		0x4000000	//
#define REASON_REVEAL		0x8000000	//
#define REASON_LINK			0x10000000	//
#define REASON_LOST_OVERLAY	0x20000000	//


# class BUFF(MyEnum):
#     addAttr="addAttr"
#     changeAtkTo="changeAtkTo"
#     cantDirectAttack="cantDirectAttack"
#     cantSacrificed="cantSacrificed"

class EFF_DURATION(MyEnum):
    onceForever=1 #but leaving hand/field/deck will reset
    utilTurnEnds=2
    utilNextTurnEnds=3
    utilMyTurnEnds=4
    utilNextMyTurnEnds=5
    utilOppositeTurnEnds=6
    utilBattleEnds=7
    fromSource=10


class SHORT_EFFECT(MyEnum):
    HERO="HERO"



class COUNT_LIMIT(MyEnum):
    sameNameOncePerTurn=-1
    unlimited=-8
    onlyOncePerDuel=-9

    oncePerTurn=1
    twicePerTurn=2
    threeTimesPerTurn=3
    fourTimesPerTurn=4




class SIGNAL_RESULT:
    none=0
    useEffect=1

class ATTACK_TYPE(MyEnum):
    none=0
    attack=0x01
    ranged=0x02
    # playerDecide=0x80


class TITLE(MyEnum):
    none=""
    auto="auto"
    target="title_target"
    damage="title_damage"
    tribute="title_tribute"
    banish="title_banish"
    destroy="title_destroy"
    changeController="title_changeController"
    returnToHand="title_returnToHand"
    returnToDeck="title_returnToDeck"
    addToHand="title_addToHand"
    sendToGrave="title_sendToGrave"
    discard="title_discard"
    specialSummon="title_specialSummon"
    fusionSummon="title_fusionSummon"
    specialSummonToEnemy="title_specialSummonToEnemy"
    selectEffect="title_selectEffect"
    equip="title_equip"
    shouldActivate="title_shouldActivate"
    changeForm="title_changeForm"
    #functional
    decideWhoFirst="decideWhoFirst"
    pleaseArrangeEffects="pleaseArrangeEffects"
    pleaseSelectEffectToActivate="pleaseSelectEffectToActivate"
    inBattleCanActivate="titleshort_canActivate"

class AI_HINT(MyEnum):
    summonSelf="this effect will activate while summoning self"
    summoner="this effect will summon monster"
    eraser="this effect will erase monster"
    damager= "this effect will damage monster"
    addAtk= "this effect will add Atk"
    costMonster="this effect will cost my monster"
    costHand="this effect will cost my hand"
    targetAll="this effect will affect all players"
    enhance="enhance"
    debuff="debuff"
    spellDestroyer="this effect will destroy spell"
    earn="this effect will earn card"
    searchMonster="this effect will search monster"
    search="this effect will search card"
    highCost="this effect cost much"
    hardToSummon="this card is hard to summon"
    botDontUse="dont use this effect"
    drawCard="drawCard"
    blockNewMonster="blockNewMonster"
    battleBenefit="battleBenefit"
    recoverLP="you will recover LP"
    permanent="permanent"


#I2 translation,text located in ALL_DATA.json
class I2(MyEnum):
    OK="OK"
    CANCEL="CANCEL"
    sendToGrave="sendToGrave"
    banish="banish"


class DEFAULT_RESULT(MyEnum):
    random="random"
    weakest="weakest"
    strongest="strongest"


