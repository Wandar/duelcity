# -*- coding: utf-8 -*-
from card_effects.cardTemplate import *
from card_effects.debugCards import *

"""
In order to modify the deck, you can copy the key from ALL_DATA.json, or you can import the classes from cardPack
"""
DEBUG_DECK1={
    "a":[
        "StumpEnt_Autumn",                # 小木桩           LV1  atk=600  diameter=1.44
        "StumpEnt_Autumn",
        "ms04_01_Minotaur_2",
        "cartoonWyvern",
        "cartoonDragon",
        "StumpEnt_Autumn",
        "ms07_Wildboar_1",                # 花冠小猪         LV1  atk=700  diameter=1.51
        "ms07_Wildboar_1",
        "ms07_Wildboar_1",
        "Sun Blossom",                    # 向阳翼花小妖     LV1  atk=800  diameter=1.36
        "Sun Blossom",
        "Sun Blossom",
        "ms04_01_Minotaur_2",             # 牛头小战士       LV2  atk=800  diameter=2.01
        "ms04_01_Minotaur_2",
        "Sci-Fi Insect Mosquito Skin2",   # 机械吸血蚊       LV2  atk=800  diameter=1.60
        "Sci-Fi Insect Mosquito Skin2",
        "Sci-Fi Insect Mosquito Skin2",
        "PlatypusA",                      # 水缘鸭嘴兽       LV2  atk=800  diameter=1.45
        "PlatypusA",
        "PlatypusA",
        "Assault Mech_Skin1",             # 铁壁推进者       LV2  atk=900  diameter=1.90
        "Assault Mech_Skin1",
        "Assault Mech_Skin1",
        "cartoonWyvern",                  # 小红龙           LV2  atk=900  diameter=3.50
        "cartoonWyvern",
        "Wolf_3",                         # 裂冰之爪         LV2  atk=900  diameter=1.79
        "Wolf_3",
        "Wolf_3",
        "cartoonDragon",                  # 小紫龙           LV2  atk=900  diameter=2.64
        "cartoonDragon",
        "ma001_Eagle_2",                  # 疾风鹰           LV2  atk=900  diameter=1.52
        "ma001_Eagle_2",
        "ma001_Eagle_2",
        "SK_BabyDragon",                  # 星芽小龙         LV2  atk=900  diameter=1.40
        "SK_BabyDragon",
        "Tiger_Black",                    # 暗影虎           LV2  atk=900  diameter=1.55
        "Tiger_Black",
        "Tiger_Black",
        "Spore",                          # 孢子球           LV1  atk=900  diameter=1.64
    ],
    "b":[
    ]
}



TUTORIAL_ENEMY_DECK={
    "a":[
        # LV<=4 且 disable=9，diameter>=1.3，atk尽可能低（共40张）
        "StumpEnt_Autumn",                # 小木桩           LV1  atk=600  diameter=1.44
        "StumpEnt_Autumn",
        "ms04_01_Minotaur_2",
        "cartoonWyvern",
        "cartoonDragon",
        "StumpEnt_Autumn",
        "ms07_Wildboar_1",                # 花冠小猪         LV1  atk=700  diameter=1.51
        "ms07_Wildboar_1",
        "ms07_Wildboar_1",
        "Sun Blossom",                    # 向阳翼花小妖     LV1  atk=800  diameter=1.36
        "Sun Blossom",
        "Sun Blossom",
        "ms04_01_Minotaur_2",             # 牛头小战士       LV2  atk=800  diameter=2.01
        "ms04_01_Minotaur_2",
        "Sci-Fi Insect Mosquito Skin2",   # 机械吸血蚊       LV2  atk=800  diameter=1.60
        "Sci-Fi Insect Mosquito Skin2",
        "Sci-Fi Insect Mosquito Skin2",
        "PlatypusA",                      # 水缘鸭嘴兽       LV2  atk=800  diameter=1.45
        "PlatypusA",
        "PlatypusA",
        "Assault Mech_Skin1",             # 铁壁推进者       LV2  atk=900  diameter=1.90
        "Assault Mech_Skin1",
        "Assault Mech_Skin1",
        "cartoonWyvern",                  # 小红龙           LV2  atk=900  diameter=3.50
        "cartoonWyvern",
        "Wolf_3",                         # 裂冰之爪         LV2  atk=900  diameter=1.79
        "Wolf_3",
        "Wolf_3",
        "cartoonDragon",                  # 小紫龙           LV2  atk=900  diameter=2.64
        "cartoonDragon",
        "ma001_Eagle_2",                  # 疾风鹰           LV2  atk=900  diameter=1.52
        "ma001_Eagle_2",
        "ma001_Eagle_2",
        "SK_BabyDragon",                  # 星芽小龙         LV2  atk=900  diameter=1.40
        "SK_BabyDragon",
        "Tiger_Black",                    # 暗影虎           LV2  atk=900  diameter=1.55
        "Tiger_Black",
        "Tiger_Black",
        "Spore",                          # 孢子球           LV1  atk=900  diameter=1.64
    ]
}


TUTORIAL_DECK={
    "a":[
        "Bass_LOD0",                      # LV1 ATK1500
        "Bass_LOD0",
        "Shoebill_LOD0",                  # LV1 ATK1600
        "Shoebill_LOD0",
        "Catfish_LOD0",

        "toon_RedPanda",                  # LV4 ATK1900
        "toon_HornedLizard",
        "toon_SnappingTurtle",            # LV4 ATK1800
        "Bull_LOD0",
        "Llama_LOD0",
        "Lynx_LOD0",                      # LV4 ATK1800
        "Walrus_LOD0",                    # LV4 ATK1800
        "SeaLion_LOD0",                   # LV4 ATK1800
        "Bull_LOD0",                      # LV4 ATK1900
        "Llama_LOD0",                     # LV4 ATK1900
        "Lynx_LOD0",
        "toon_HornedLizard",              # LV4 ATK1900
        "toon_RedPanda",
        "toon_SnappingTurtle",
        # ── LV1 (ATK 1500-1600) ──────────────────────────

        # ── LV2 (ATK 1500-1600) ──────────────────────────
        "Catfish_LOD0",                   # LV2 ATK1600

        "Echidna_LOD0",                   # LV2 ATK1500
        "FlyingFox_LOD0",                 # LV2 ATK1500
        "Giraffe_LOD0",                   # LV2 ATK1600
        "Goat_LOD0",                      # LV2 ATK1550
        "Goat_LOD0",
        "Toucan_LOD0",                    # LV2 ATK1550
        # ── LV3 (ATK 1700-1800) ──────────────────────────
        "Goose_LOD0",                     # LV3 ATK1700
        "Goose_LOD0",
        "Turkey_LOD0",                    # LV3 ATK1800
        "Turkey_LOD0",
        # ── LV4 (ATK 1800-1900) ──────────────────────────

        # ── LV5 (ATK 2100-2400) ──────────────────────────
        "Elephant_LOD0",                  # LV5 ATK2200
        "Elephant_LOD0",
        "Moose_LOD0",                     # LV5 ATK2400
        "Moose_LOD0",
        "toon_Crocodile",                 # LV5 ATK2300
        "toon_Crocodile",
        "toon_Hedgehog",                  # LV5 ATK2300
        "toon_Raccoon",                   # LV5 ATK2100
        "toon_Skunk",                     # LV5 ATK2200
        # ── LV6 (ATK 2600) ───────────────────────────────
        "toon_Lobster",                   # LV6 ATK2600
        "toon_Lobster",
    ],
    "b":[
    ]
}



DEBUG_DECK2={
    "a":[
        "Dark Knight",
        "Character_Color_03",
        "ghoul",
        "ghoul_scavenger",
        "DragonBoss",
        "Basilisk1",
        "DragonBug",
        "angel wing",
        "angel wing",
        "angel wing",
        "angel wing",
        "angel wing",
        "DragonWorm",
        "PlantMonsterRed",
        "OakTreeEnt",
        # "Satyr_DualWield",
        # "ghoul",
        # "Hydra",
        # "Hydra",
        # ghoul_grotesque,
        # ghoul,
        # ghoul_boss,
        # ghoul_boss,
        # ghoul_boss,
        # ghoul_boss,
        # ghoul_boss,
        # ghoul,
        # ghoul_boss,
        # ghoul,
        # ghoul_boss
    ],
    "b":[
        "GolemRock"
    ]
}


NEWBIE_DECK1={
    # 主题：风系/地系 低级入门（机械+兽战士，低等级居多）共40张
    "a":[
        "Whirlwind",            # 微风小精灵   LV1  FAIRY/WIND
        "Whirlwind",
        "GridRobot",            # 浮游机       LV2  MACHINE/WIND
        "GridRobot",
        "JellyfishRobot",       # 水母机       LV2  MACHINE/WIND
        "JellyfishRobot",
        "BotRo",                # 巡游机器     LV2  MACHINE/WIND
        "BotRo",
        "cartoonLeviathan",     # 小绿龙       LV2  DRAGON/GRASS
        "cartoonLeviathan",
        "ms01_Golem_1",         # 石头小傀儡   LV2  ROCK/EARTH
        "ms01_Golem_1",
        "ms02_Stump_1",         # 树桩怪       LV2  PLANT/GRASS
        "ms02_Stump_1",
        "ms04_01_Minotaur_2",   # 牛头小战士   LV2  BEASTWARRIOR/DARK
        "ms04_01_Minotaur_2",
        "SKM_Iron_Golem",       # 重甲石傀儡   LV2
        "SKM_Iron_Golem",
        "WerewolfMaskTint",     # 獠牙勇士     LV3  BEASTWARRIOR/EARTH
        "WerewolfMaskTint",
        "RatAssassinDefault",   # 鼠兵         LV3  BEASTWARRIOR/EARTH
        "RatAssassinDefault",
        "Ankylosaurus",         # 甲龙         LV3  DINOSAUR/EARTH
        "Ankylosaurus",
        "Turkey_LOD0",          # 咯咯火鸡     LV3  WINDBEAST/WIND
        "Turkey_LOD0",
        "NexusRobot",           # 联集卫士     LV3  MACHINE/WIND
        "NexusRobot",
        "Kitsune_2",            # 浣熊骑士     LV3  BEASTWARRIOR/LIGHT
        "Kitsune_2",
        "ThreeTailedWolf",      # 三尾雪狼     LV4  BEAST/WATER
        "ThreeTailedWolf",
        "Dragonide",            # 铁锤蜥蜴     LV4  BEASTWARRIOR/EARTH
        "Dragonide",
        "toon_SnappingTurtle",  # 慢慢小龟     LV4  BEAST/GRASS
        "toon_SnappingTurtle",
        "LizardWarriorDefault", # 蜥蜴战士     LV4  REPTILE/EARTH
        "LizardWarriorDefault",
        "EnemyCreature_V1",     # 甜梦幻蜥     LV3  REPTILE/WATER
        "EnemyCreature_V1",
    ],
    "b":[]
}

NEWBIE_DECK2={
    # 主题：野兽自然系（兽族+虫族，草/水属性，中等难度）共40张
    "a":[
        "jhp_treasure_poter_ani",   # 宝藏搜寻者 LV3  BEAST/EARTH
        "jhp_treasure_poter_ani",
        "EnemyCreature_V1",         # 甜梦幻蜥   LV3  REPTILE/WATER
        "EnemyCreature_V1",
        "ms02_Stump_1",             # 树桩怪     LV2  PLANT/GRASS
        "ms02_Stump_1",
        "cartoonLeviathan",         # 小绿龙     LV2  DRAGON/GRASS
        "cartoonLeviathan",
        "Whirlwind",                # 微风小精灵 LV1  FAIRY/WIND
        "Whirlwind",
        "WerewolfMaskTint",         # 獠牙勇士   LV3  BEASTWARRIOR/EARTH
        "WerewolfMaskTint",
        "RatAssassinDefault",       # 鼠兵       LV3  BEASTWARRIOR/EARTH
        "RatAssassinDefault",
        "JapaneseHornet",           # 大黄蜂     LV4  INSECT/GRASS
        "JapaneseHornet",
        "Mantis",                   # 螳螂       LV4  INSECT/GRASS
        "Mantis",
        "ThreeTailedWolf",          # 三尾雪狼   LV4  BEAST/WATER
        "ThreeTailedWolf",
        "Ankylosaurus",             # 甲龙       LV3  DINOSAUR/EARTH
        "Ankylosaurus",
        "T Rex",                    # 暴龙       LV4  DINOSAUR/EARTH
        "T Rex",
        "toon_SnappingTurtle",      # 慢慢小龟   LV4  BEAST/GRASS
        "toon_SnappingTurtle",
        "toon_Raccoon",             # 跳跳浣熊   LV5  BEAST/GRASS
        "toon_Raccoon",
        "toon_Crocodile",           # 凶凶鳄鱼   LV5  BEAST/GRASS
        "toon_Crocodile",
        "toon_Hedgehog",            # 滚滚刺猬   LV5  BEAST/GRASS
        "toon_Hedgehog",
        "StoneBeast",               # 蓝晶甲壳兽 LV4  AQUA/WATER
        "StoneBeast",
        "CrystalElemental_Cave",    # 水晶元素   LV7  ROCK/WATER
        "CrystalElemental_Cave",
        "cartoonCerberus",          # 爪爪守卫   LV7  BEAST/DARK
        "cartoonCerberus",
        "ms01_Golem_1",             # 石头小傀儡 LV2  ROCK/EARTH
        "ms01_Golem_1",
    ],
    "b":[]
}

NEWBIE_DECK3={
    # 主题：龙族机战（龙族+高攻机械，高等级大怪）共40张
    "a":[
        "GridRobot",                # 浮游机         LV2  MACHINE/WIND
        "GridRobot",
        "JellyfishRobot",           # 水母机         LV2  MACHINE/WIND
        "JellyfishRobot",
        "BotRo",                    # 巡游机器       LV2  MACHINE/WIND
        "BotRo",
        "NexusRobot",               # 联集卫士       LV3  MACHINE/WIND
        "NexusRobot",
        "ms04_01_Minotaur_2",       # 牛头小战士     LV2  BEASTWARRIOR/DARK
        "ms04_01_Minotaur_2",
        "SKM_Iron_Golem",           # 重甲石傀儡     LV2
        "SKM_Iron_Golem",
        "smallDragonWhelp_Rd",      # 熔岩雏龙       LV4  DRAGON/FIRE
        "smallDragonWhelp_Rd",
        "JapaneseHornet",           # 大黄蜂         LV4  INSECT/GRASS
        "JapaneseHornet",
        "Mantis",                   # 螳螂           LV4  INSECT/GRASS
        "Mantis",
        "EnemyCreature_V1",         # 甜梦幻蜥       LV3  REPTILE/WATER
        "EnemyCreature_V1",
        "Kitsune_2",                # 浣熊骑士       LV3  BEASTWARRIOR/LIGHT
        "Kitsune_2",
        "jhp_treasure_poter_ani",   # 宝藏搜寻者     LV3  BEAST/EARTH
        "jhp_treasure_poter_ani",
        "Dragon Bot",               # 灵巧机龙       LV5  MACHINE/FIRE
        "Dragon Bot",
        "toon_Raccoon",             # 跳跳浣熊       LV5  BEAST/GRASS
        "toon_Raccoon",
        "toon_Crocodile",           # 凶凶鳄鱼       LV5  BEAST/GRASS
        "toon_Crocodile",
        "toon_Hedgehog",            # 滚滚刺猬       LV5  BEAST/GRASS
        "toon_Hedgehog",
        "MountainDragon",           # 地褐角龙       LV7  DRAGON/FIRE
        "MountainDragon",
        "cartoonChineseDragon",     # 漩漩雷云       LV7  DRAGON/WIND
        "cartoonChineseDragon",
        "cartoonCerberus",          # 爪爪守卫       LV7  BEAST/DARK
        "cartoonCerberus",
        "Pref_LittleEvilDragon",    # 小邪龙         LV7  DRAGON/DARK
        "Pref_LittleEvilDragon",
    ],
    "b":[]
}


DECK_BOT={
    "a":[

    ],
    "b":[

    ]
}


# ============================================================
# ELITE_DECK_DRAGON  —  暗龙皇
# 主题: 全 bt=5/4 龙族, 由低级卡通龙垫场, 招牌大龙收尾
# bt=5 小怪: cartoonWyvern/cartoonDragon/cartoonLeviathan(LV2, bt=3)
# bt=5 中怪: Pref_CuteDragon(LV7), Wyrm1_2(LV7, bt=4)
# bt=5 招牌: dragonrex(LV8,3300), Wyvern(LV8,2700), polardragon(LV8,2750),
#            cartoonChineseDragon(LV7,2500), Mdl_Monster000_0002(LV12,4400)
#            Mdl_Monster003_0001(LV12,4200), Mdl_Monster000_0000(LV12,4200)
# ============================================================
ELITE_DECK_DRAGON={
    "a":[
        # ── LV4-5 中级龙 (bt=3~4) ──────────────────────────────
        "Drake Skinny",                   # 渊蓝龙人       LV4  ATK=1500  bt=3  DRAGON/WATER
        "Drake Skinny",
        "Drake Realistic",                # 烈焰龙人       LV5  ATK=1700  bt=3  DRAGON/FIRE
        "Drake Realistic",
        "ForestDrake_Blue",               # 森林妖龙       LV4  ATK=1300  bt=2  DRAGON/GRASS
        "ForestDrake_Blue",
        # ── LV7 精英龙 (bt=4~5) ────────────────────────────────
        "Pref_CuteDragon",                # 小斧龙         LV7  ATK=2300  bt=5  DRAGON/GRASS
        "Pref_CuteDragon",
        "Wyrm1_2",                        # 碧空晶蜥       LV7  ATK=2400  bt=4  DRAGON/GRASS
        "cartoonChineseDragon",           # 漩漩雷云       LV7  ATK=2500  bt=5  DRAGON/WIND
        # ── LV7-8 招牌大龙 (bt=4~5) ────────────────────────────
        "MountainDragon",                 # 地褐角龙       LV7  ATK=2600  bt=3  DRAGON/FIRE
        "plainsdragon",                   # 牧野之龙       LV8  ATK=2700  bt=4  DRAGON/EARTH
        "Wyvern",                         # 暴君龙         LV8  ATK=2700  bt=4  DRAGON/WIND
        "polardragon",                    # 冰晶之龙       LV8  ATK=2750  bt=5  DRAGON/WATER
        "dragonrex",                      # 恐暴龙         LV8  ATK=3300  bt=5  DRAGON/EARTH
        # ── LV12 超级招牌 (bt=5) ───────────────────────────────
        "Mdl_Monster000_0000",            # 金焰熔岩龙     LV12 ATK=4200  bt=5  DRAGON/FIRE
        "Mdl_Monster003_0001",            # 轰鸣雷暴龙     LV12 ATK=4200  bt=5  DRAGON/LIGHT
        "Mdl_Monster000_0002",            # 虹羽风暴龙     LV12 ATK=4400  bt=5  DRAGON/WIND
    ],
    "b":[]
}


# ============================================================
# ELITE_DECK_MECH  —  机甲军团
# 主题: 全 bt=5/4 机械族, 百兽机四件套打底, 顶级机械压制
# bt=5 低级: SciFi Beast06(LV4,1600) ~ SciFi Beast03(LV4,1800)
# bt=5 招牌: SK_VelociraptorMech(LV7,2400), SkyMecha(LV8,2700),
#            Sci-Fi Dragon Skin4(LV8,2800), Dragon Predator Robot(LV10,3400)
# ============================================================
ELITE_DECK_MECH={
    "a":[
        # ── LV4 百兽机四件套 (bt=5) ────────────────────────────
        "SciFi Beast06 Bull Skin2",       # 百兽机 牛怪    LV4  ATK=1600  bt=5  MACHINE/LIGHT
        "SciFi Beast06 Bull Skin2",       # 百兽机 牛怪    LV4  ATK=1600  bt=5  MACHINE/LIGHT
        "SciFi Beast06 Bull Skin2",
        "SciFi Beast05_Skin1",            # 百兽机 暴龙    LV4  ATK=1700  bt=5  MACHINE/LIGHT
        "SciFi Beast05_Skin1",            # 百兽机 暴龙    LV4  ATK=1700  bt=5  MACHINE/LIGHT
        "SciFi Beast05_Skin1",
        "SciFi Beast04 WhaleSnake Skin1", # 百兽机 黑鲸    LV4  ATK=1800  bt=5  MACHINE/LIGHT
        "SciFi Beast04 WhaleSnake Skin1",
        "SciFi Beast04 WhaleSnake Skin1",
        "SciFi Beast03 Skin1",            # 百兽机 翼龙    LV4  ATK=1800  bt=5  MACHINE/LIGHT
        "SciFi Beast03 Skin1",
        "SciFi Beast03 Skin1",
        # ── LV4 额外机甲 (bt=3) ────────────────────────────────
        "ACS17",                          # 机甲17         LV4  ATK=1500  bt=3  MACHINE/EARTH
        "ACS17",
        "droid",                          # 迷彩机甲兵     LV4  ATK=1400  bt=3  MACHINE/EARTH
        "droid",
        "droid",
        # ── LV5 中级机甲 (bt=4) ────────────────────────────────
        "Dragon Bot",                     # 灵巧机龙       LV5  ATK=1900  bt=4  MACHINE/FIRE
        "Razor Robot",
        # ── LV7-10 招牌大机甲 (bt=5) ───────────────────────────
        "SK_VelociraptorMech",            # 机器速龙       LV7  ATK=2400  bt=5  MACHINE/WIND
        "SkyMecha",                       # 天穹守护者     LV8  ATK=2700  bt=5  MACHINE/LIGHT
        "Sci-Fi Dragon Skin4",            # 百兽机 辰龙    LV8  ATK=2800  bt=5  MACHINE/LIGHT
        "Dragon Predator Robot",          # 捕食机龙       LV10 ATK=3400  bt=5  MACHINE/FIRE
    ],
    "b":[]
}


# ============================================================
# ELITE_DECK_BEAST  —  百兽霸主
# 主题: bt=5/4 兽族/恐龙/战士混合, 高攻场均
# bt=5 小怪: SM_EnemyGoblin(LV3,1500), EnemyCreature_V1(LV3,1400)
# bt=5 中怪: Beast_1(LV4,1900), StoneBeast(LV4,2000)
# bt=4 恐龙: T Rex(LV4,1900), Dilophosaurus(LV4,1600), toon_Crocodile(LV5,1900)
# bt=5 招牌: SwordsTiger(LV6,2000), cartoonCerberus(LV7,2300),
#            cartoonKirin(LV7,2300), GhostTiger(LV9,3200)
# ============================================================
ELITE_DECK_BEAST={
    "a":[
        # ── LV1-3 小怪垫场 (bt=4~5) ────────────────────────────
        "Dino_Cat_04",                    # 小龙猫         LV1  ATK=900   bt=4  BEAST/LIGHT
        "Dino_Cat_04",
        "Dino_Cat_04",
        "Dog Bark",                       # 爆火狂犬仔     LV3  ATK=1200  bt=4  BEAST/FIRE
        "Dog Bark",
        "Dog Bark",
        "SM_EnemyGoblin",                 # 绿影咕哝者     LV3  ATK=1500  bt=5  FIEND/EARTH
        "SM_EnemyGoblin",
        "SM_EnemyGoblin",
        "EnemyCreature_V1",               # 甜梦幻蜥       LV3  ATK=1400  bt=5  REPTILE/WATER
        "EnemyCreature_V1",
        "EnemyCreature_V1",
        # ── LV4 强力中怪 (bt=4~5) ──────────────────────────────
        "Beast_1",                        # 刺壳巨兽       LV4  ATK=1900  bt=5  INSECT/GRASS
        "Beast_1",
        "Beast_1",
        "StoneBeast",                     # 蓝晶甲壳兽     LV4  ATK=2000  bt=5  AQUA/WATER
        "StoneBeast",                     # 蓝晶甲壳兽     LV4  ATK=2000  bt=5  AQUA/WATER
        "StoneBeast",
        "T Rex",                          # 暴龙           LV4  ATK=1900  bt=4  DINOSAUR/EARTH
        "T Rex",                          # 暴龙           LV4  ATK=1900  bt=4  DINOSAUR/EARTH
        "T Rex",
        "Dilophosaurus",                  # 双冠龙         LV4  ATK=1600  bt=4  DINOSAUR/EARTH
        "Dilophosaurus",                  # 双冠龙         LV4  ATK=1600  bt=4  DINOSAUR/EARTH
        "Dilophosaurus",
        # ── LV5-6 上级怪 (bt=4~5) ──────────────────────────────
        "toon_Crocodile",                 # 凶凶鳄鱼       LV5  ATK=1900  bt=4  BEAST/GRASS
        "toon_Crocodile",
        "toon_Hedgehog",                  # 滚滚刺猬       LV5  ATK=1900  bt=4  BEAST/GRASS
        "Dog Bowwow",                     # 爆火狂犬       LV5  ATK=2000  bt=4  BEASTWARRIOR/FIRE
        "SwordsTiger",                    # 剑虎           LV6  ATK=2000  bt=5  BEASTWARRIOR/LIGHT
    ],
    "b":[]
}
