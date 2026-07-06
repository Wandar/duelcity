# -*- coding: utf-8 -*-
from card_effects.cardTemplate import *
from card_effects.debugCards import *

"""
In order to modify the deck, you can copy the key from ALL_DATA.json, or you can import the classes from cardPack
"""
DEBUG_DECK1={
    "a":[
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
    # 对方:攻击力低,LV<=4,不重复,共40张(32怪+8魔陷)
    "a":[
        "ms07_Wildboar_1",                 # 花冠小猪           LV1 atk700   btNone dia1.5142
        "ms04_01_Minotaur_2",              # 牛头小战士          LV2 atk800   btNone dia2.0064
        "Sci-Fi Insect Mosquito Skin2",    # 机械吸血蚊          LV2 atk800   bt4 dia1.6
        "PlatypusA",                       # 水缘鸭嘴兽          LV2 atk800   btNone dia1.449
        "Sun Blossom",                     # 向阳翼花小妖         LV1 atk800   bt2 dia1.36
        "cartoonWyvern",                   # 小红龙            LV2 atk900   bt3 dia3.5
        "cartoonDragon",                   # 小紫龙            LV2 atk900   bt3 dia2.64
        "Assault Mech_Skin1",              # 铁壁推进者          LV2 atk900   bt4 dia1.898
        "Wolf_3",                          # 裂冰之爪           LV2 atk900   bt4 dia1.7854
        "Spore",                           # 孢子球            LV1 atk900   btNone dia1.638
        "Tiger_Black",                     # 暗影虎            LV2 atk900   btNone dia1.55
        "ma001_Eagle_2",                   # 疾风鹰            LV2 atk900   btNone dia1.5196
        "Sci-Fi_Robot_Spider Prefab",      # 量子侦察蛛          LV2 atk900   bt4 dia1.49
        "SK_BabyDragon",                   # 星芽小龙           LV2 atk900   btNone dia1.3975
        "ms01_Golem_1",                    # 石头小傀儡          LV2 atk1000  btNone dia2.2064
        "Sci-Fi Insect Miner Beetle Skin1", # 旋轮机虫           LV3 atk1000  bt3 dia2.01
        "WerewolfMaskTint",                # 獠牙勇士           LV3 atk1000  bt1 dia1.84
        "SKM_Iron_Golem",                  # 重甲石傀儡          LV2 atk1000  bt3 dia1.575
        "ms02_Stump_1",                    # 树桩怪            LV2 atk1000  btNone dia1.519
        "Big Draco Ground 04",             # 重壳巨龙龟          LV3 atk1000  bt3 dia1.472
        "TankerRobot",                     # 动力钢铁           LV3 atk1100  bt2 dia2.56
        "FireGolem_03",                    # 沼泽泥巨人          LV3 atk1100  bt4 dia2.45
        "KingSlime_1",                     # 史莱姆国王          LV3 atk1100  bt4 dia1.7625
        "CrabMonsterDefault",              # 迷你螃蟹           LV2 atk1100  bt0 dia1.6
        "jhp_treasure_poter_ani",          # 宝藏搜寻者          LV3 atk1100  bt2 dia1.3
        "Cactus Boss",                     # 巨嘴刺王           LV3 atk1200  bt3 dia4.6
        "Werewolf",                        # 寒蓝恶狼           LV3 atk1200  bt3 dia3.0
        "OrcPBR",                          # 锤炼小兽人          LV2 atk1200  bt3 dia2.5
        "Dragon Inferno",                  # 爆炎小恶龙          LV3 atk1200  btNone dia2.3
        "Treant_Summer",                   # 夏日树妖           LV4 atk1200  bt1 dia1.96
        "Flying_Golem",                    # 飞行魔像           LV3 atk1200  bt2 dia1.5
        # ── 魔法/陷阱 ──
        "43foot",                          # 捕兽陷阱           [魔陷]
        "50coin",                          # 命运金币           [魔陷]
        "151search",                       # 密林搜寻           [魔陷]
        "096wind",                         # 风之传送阵          [魔陷]
        "behindtree",                      # 密林伏击           [魔陷]
        "T_Druid8",                        # 藤蔓缠绕           [魔陷]
        "49flyshoe",                       # 疾风飞靴           [魔陷]
        "T_Card_Ico_shadow_hand",          # 阴影之手           [魔陷]
    ],
    "b":[
    ]
}

TUTORIAL_DECK={
    # 我方:高bt在上,LV<=4易召唤,不重复,共40张(32怪+8魔陷)
    "a":[
        "StoneBeast",                      # 蓝晶甲壳兽          LV4 atk2000  bt5 dia2.2
        "Beast_1",                         # 刺壳巨兽           LV4 atk1900  bt5 dia2.85
        "SKM_whale",                       # 机器鲸鱼           LV4 atk1800  bt5 dia1.4
        "Griffin_skin",                    # 幽暗森林 守林狮鹫      LV4 atk1800  bt5 dia3.0
        "SciFi Beast03 Skin1",             # 百兽机 翼龙         LV4 atk1800  bt5 dia4.8
        "SciFi Beast04 WhaleSnake Skin1",  # 百兽机 黑鲸         LV4 atk1800  bt5 dia4.5
        "SciFi Beast05_Skin1",             # 百兽机 暴龙         LV4 atk1700  bt5 dia3.6
        "SciFi Beast06 Bull Skin2",        # 百兽机 牛怪         LV4 atk1600  bt5 dia2.8
        "T Rex",                           # 暴龙             LV4 atk1900  bt4 dia1.408
        "Brachiosaurus",                   # 腕龙             LV4 atk1600  bt4 dia2.15
        "Dilophosaurus",                   # 双冠龙            LV4 atk1600  bt4 dia1.52
        "Triceratops",                     # 三角龙            LV3 atk1500  bt4 dia1.34
        "Ankylosaurus",                    # 甲龙             LV3 atk1500  bt4 dia1.69
        "Stegosaurus",                     # 剑龙             LV3 atk1400  bt4 dia1.98
        "Mosasaurus",                      # 沧龙             LV3 atk1300  bt4 dia1.864
        "Ent",                             # 林间巨灵           LV3 atk1300  bt4 dia2.5
        "FireMeka_01",                     # 赤焰机甲兽          LV4 atk1300  bt4 dia2.7824
        "FireGolem_03",                    # 沼泽泥巨人          LV3 atk1100  bt4 dia2.45
        "KingSlime_1",                     # 史莱姆国王          LV3 atk1100  bt4 dia1.7625
        "Assault Mech_Skin1",              # 铁壁推进者          LV2 atk900   bt4 dia1.898
        "Sci-Fi_Robot_Spider Prefab",      # 量子侦察蛛          LV2 atk900   bt4 dia1.49
        "Wolf_3",                          # 裂冰之爪           LV2 atk900   bt4 dia1.7854
        "Sci-Fi Insect Mosquito Skin2",    # 机械吸血蚊          LV2 atk800   bt4 dia1.6
        "Caterpillar",                     # 毛毛虫            LV4 atk1600  bt3 dia1.4
        "ACS17",                           # 机甲17           LV4 atk1500  bt3 dia1.44
        "Drake Skinny",                    # 渊蓝龙人           LV4 atk1500  bt3 dia1.76
        "Ladybug",                         # 七星瓢虫           LV4 atk1400  bt3 dia1.3
        "Dragonknight",                    # 赤鳞龙骑士          LV4 atk1400  bt3 dia1.958
        "Werewolf",                        # 寒蓝恶狼           LV3 atk1200  bt3 dia3.0
        "Cactus Boss",                     # 巨嘴刺王           LV3 atk1200  bt3 dia4.6
        "OrcPBR",                          # 锤炼小兽人          LV2 atk1200  bt3 dia2.5
        "Sci-Fi Insect Miner Beetle Skin1", # 旋轮机虫           LV3 atk1000  bt3 dia2.01
        # ── 魔法/陷阱 ──
        "48wing",                          # 炽天使之翼          [魔陷]
        "T_Card_Ico_multi_cast",           # 多重施法           [魔陷]
        "T_Card_Ico_ball_lightning",       # 球形闪电           [魔陷]
        "T_Cryomancer9",                   # 寒冰爆发           [魔陷]
        "T_Card_Ico_rainbow",              # 彩虹多样           [魔陷]
        "thegolem",                        # 魔像降临           [魔陷]
        "429sword",                        # 新月之刃           [魔陷]
        "48fly",                           # 彩蝶秘瓶           [魔陷]
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
    # 入门:机械+兽战士(20低+10高+10魔陷=40张)
    "a":[
        # ── LV<=4 (20) ──
        "ms04_01_Minotaur_2",              # 牛头小战士        LV2 atk800   BEASTWARRIOR
        "Sci-Fi Insect Mosquito Skin2",    # 机械吸血蚊        LV2 atk800   MACHINE
        "GridRobot",                       # 浮游机          LV2 atk900   MACHINE
        "ms06_Rat_1",                      # 大耳鼠射手        LV2 atk900   BEASTWARRIOR
        "ToonRobot (25)",                  # 蓝装巡逻机        LV2 atk900   MACHINE
        "Sci-Fi_Robot_Spider Prefab",      # 量子侦察蛛        LV2 atk900   MACHINE
        "JellyfishRobot",                  # 水母机          LV2 atk1000  MACHINE
        "WerewolfMaskTint",                # 獠牙勇士         LV3 atk1000  BEASTWARRIOR
        "Sci-Fi Insect Miner Beetle Skin1", # 旋轮机虫         LV3 atk1000  MACHINE
        "TankerRobot",                     # 动力钢铁         LV3 atk1100  MACHINE
        "RatAssassinDefault",              # 鼠兵           LV3 atk1100  BEASTWARRIOR
        "BotRo",                           # 巡游机器         LV2 atk1200  MACHINE
        "OrcPBR",                          # 锤炼小兽人        LV2 atk1200  BEASTWARRIOR
        "Kitsune_2",                       # 浣熊骑士         LV3 atk1200  BEASTWARRIOR
        "NexusRobot",                      # 联集卫士         LV3 atk1300  MACHINE
        "droid",                           # 迷彩机甲兵        LV4 atk1400  MACHINE
        "ACS17",                           # 机甲17         LV4 atk1500  MACHINE
        "SciFi Beast06 Bull Skin2",        # 百兽机 牛怪       LV4 atk1600  MACHINE
        "FireMeka_01",                     # 赤焰机甲兽        LV4 atk1600  MACHINE
        "SciFi Beast05_Skin1",             # 百兽机 暴龙       LV4 atk1700  MACHINE
        # ── LV>=5 (10) ──
        "Dragonrace",                      # 巨爪龙兽         LV5 atk2400  MACHINE
        "Dog Bowwow",                      # 爆火狂犬         LV5 atk2000  BEASTWARRIOR
        "Dragon Bot",                      # 灵巧机龙         LV5 atk1900  MACHINE
        "Razor Robot",                     # 刺轮战机         LV5 atk1800  MACHINE
        "MechaGolem_Bronze",               # 古代青铜机械       LV5 atk1700  MACHINE
        "Sci-Fi Mantis_Skin1",             # 刃翼螳螂         LV5 atk1600  MACHINE
        "Sci-Fi Insect StagBeetle Skin3",  # 机械锹形虫        LV5 atk1400  MACHINE
        "SwordsTiger",                     # 剑虎           LV6 atk2000  BEASTWARRIOR
        "Dragon7_basemesh1",               # 黄金机骸龙        LV7 atk2500  MACHINE
        "SK_VelociraptorMech",             # 机器速龙         LV7 atk2400  MACHINE
        # ── 魔法/陷阱 (10) ──
        "429sword",                        # 新月之刃         [魔陷]
        "48fly",                           # 彩蝶秘瓶         [魔陷]
        "50coin",                          # 命运金币         [魔陷]
        "151search",                       # 密林搜寻         [魔陷]
        "thegolem",                        # 魔像降临         [魔陷]
        "T_Card_Ico_ball_lightning",       # 球形闪电         [魔陷]
        "T_Card_Ico_multi_cast",           # 多重施法         [魔陷]
        "43foot",                          # 捕兽陷阱         [魔陷]
        "48wing",                          # 炽天使之翼        [魔陷]
        "T_Card_Ico_rainbow",              # 彩虹多样         [魔陷]
    ],
    "b":[]
}

NEWBIE_DECK2={
    # 自然:兽+虫+植物(20低+10高+10魔陷=40张)
    "a":[
        # ── LV<=4 (20) ──
        "StumpEnt_Autumn",                 # 小木桩          LV1 atk600   PLANT
        "ms03_Bee_1",                      # 小蜜蜂          LV1 atk600   INSECT
        "Bizun_2",                         # 棘丛暴獠         LV1 atk600   BEAST
        "ms07_Wildboar_1",                 # 花冠小猪         LV1 atk700   BEAST
        "Sun Blossom",                     # 向阳翼花小妖       LV1 atk800   PLANT
        "Bizun_1",                         # 棘丛小暴獠        LV1 atk800   BEAST
        "PlatypusA",                       # 水缘鸭嘴兽        LV2 atk800   BEAST
        "CombatCat01",                     # 夜林潜行喵        LV3 atk800   BEAST
        "Dino_Cat_04",                     # 小龙猫          LV1 atk900   BEAST
        "Spore",                           # 孢子球          LV1 atk900   PLANT
        "cartoonPegasus",                  # 光辉小马         LV2 atk900   BEAST
        "Tiger_Black",                     # 暗影虎          LV2 atk900   BEAST
        "Cat Bolt",                        # 红闪电猫         LV2 atk1000  BEAST
        "Cat Lightning",                   # 黄闪电猫         LV2 atk1000  BEAST
        "ms02_Stump_1",                    # 树桩怪          LV2 atk1000  PLANT
        "BunnyRat",                        # 雪兔           LV3 atk1000  BEAST
        "jhp_treasure_poter_ani",          # 宝藏搜寻者        LV3 atk1100  BEAST
        "Werewolf",                        # 寒蓝恶狼         LV3 atk1200  BEAST
        "Cactus Boss",                     # 巨嘴刺王         LV3 atk1200  PLANT
        "Dog Bark",                        # 爆火狂犬仔        LV3 atk1200  BEAST
        # ── LV>=5 (10) ──
        "Moose_LOD0",                      # 大角驼鹿         LV5 atk2400  BEAST
        "toon_Crocodile",                  # 凶凶鳄鱼         LV5 atk2300  BEAST
        "toon_Hedgehog",                   # 滚滚刺猬         LV5 atk2300  BEAST
        "toon_Skunk",                      # 坏坏臭鼬         LV5 atk2200  BEAST
        "Sunflora Pixie",                  # 向阳翼花王        LV5 atk2200  PLANT
        "Elephant_LOD0",                   # 灵鼻象          LV5 atk2200  BEAST
        "GiantBeetle",                     # 萤光舞翼         LV5 atk2100  INSECT
        "toon_Raccoon",                    # 跳跳浣熊         LV5 atk2100  BEAST
        "RhinocerosBeetle",                # 甲虫           LV5 atk1700  INSECT
        "Unicorn_Pegasus",                 # 独角兽珀加索斯      LV6 atk2300  BEAST
        # ── 魔法/陷阱 (10) ──
        "T_Druid8",                        # 藤蔓缠绕         [魔陷]
        "behindtree",                      # 密林伏击         [魔陷]
        "096wind",                         # 风之传送阵        [魔陷]
        "48wing",                          # 炽天使之翼        [魔陷]
        "T_Card_Ico_rainbow",              # 彩虹多样         [魔陷]
        "50coin",                          # 命运金币         [魔陷]
        "151search",                       # 密林搜寻         [魔陷]
        "T_Card_Ico_master_of_tactics",    # 战术大师         [魔陷]
        "43foot",                          # 捕兽陷阱         [魔陷]
        "T_Druid14",                       # 自然庇护         [魔陷]
    ],
    "b":[]
}

NEWBIE_DECK3={
    # 龙战:龙+机械 高攻(20低+10高+10魔陷=40张)
    "a":[
        # ── LV<=4 (20) ──
        "Sci-Fi Insect Mosquito Skin2",    # 机械吸血蚊        LV2 atk800   MACHINE
        "GridRobot",                       # 浮游机          LV2 atk900   MACHINE
        "cartoonDragon",                   # 小紫龙          LV2 atk900   DRAGON
        "cartoonLeviathan",                # 小绿龙          LV2 atk900   DRAGON
        "cartoonWyvern",                   # 小红龙          LV2 atk900   DRAGON
        "SK_BabyDragon",                   # 星芽小龙         LV2 atk900   DRAGON
        "ToonRobot (25)",                  # 蓝装巡逻机        LV2 atk900   MACHINE
        "Sci-Fi_Robot_Spider Prefab",      # 量子侦察蛛        LV2 atk900   MACHINE
        "ToonDragon_Lowpoly",              # 豆芽小飞龙        LV2 atk1000  DRAGON
        "JellyfishRobot",                  # 水母机          LV2 atk1000  MACHINE
        "Sci-Fi Insect Miner Beetle Skin1", # 旋轮机虫         LV3 atk1000  MACHINE
        "TankerRobot",                     # 动力钢铁         LV3 atk1100  MACHINE
        "BotRo",                           # 巡游机器         LV2 atk1200  MACHINE
        "Dragon Inferno",                  # 爆炎小恶龙        LV3 atk1200  DRAGON
        "NexusRobot",                      # 联集卫士         LV3 atk1300  MACHINE
        "ForestDrake_Blue",                # 森林妖龙         LV4 atk1300  DRAGON
        "Fantasy Dragon-Blue",             # 风暴亚龙         LV4 atk1300  DRAGON
        "droid",                           # 迷彩机甲兵        LV4 atk1400  MACHINE
        "smallDragonWhelp_Rd",             # 熔岩雏龙         LV4 atk1400  DRAGON
        "FireDragonRed",                   # 火龙           LV4 atk1500  DRAGON
        # ── LV>=5 (10) ──
        "Dragonrace",                      # 巨爪龙兽         LV5 atk2400  MACHINE
        "Dragon Bot",                      # 灵巧机龙         LV5 atk1900  MACHINE
        "Razor Robot",                     # 刺轮战机         LV5 atk1800  MACHINE
        "MechaGolem_Bronze",               # 古代青铜机械       LV5 atk1700  MACHINE
        "Sci-Fi Mantis_Skin1",             # 刃翼螳螂         LV5 atk1600  MACHINE
        "Sci-Fi Insect StagBeetle Skin3",  # 机械锹形虫        LV5 atk1400  MACHINE
        "Dragon_Rd",                       # 熔岩绯龙         LV6 atk1800  DRAGON
        "ElderDragon_Rd",                  # 熔岩圣龙         LV6 atk1800  DRAGON
        "MountainDragon",                  # 地褐角龙         LV7 atk2600  DRAGON
        "cartoonChineseDragon",            # 漩漩雷云         LV7 atk2500  DRAGON
        # ── 魔法/陷阱 (10) ──
        "T_Cryomancer9",                   # 寒冰爆发         [魔陷]
        "T_Card_Ico_ball_lightning",       # 球形闪电         [魔陷]
        "T_Card_Ico_multi_cast",           # 多重施法         [魔陷]
        "thegolem",                        # 魔像降临         [魔陷]
        "429sword",                        # 新月之刃         [魔陷]
        "244bigfire",                      # 龙焰浩劫         [魔陷]
        "T_Card_Ico_rainbow",              # 彩虹多样         [魔陷]
        "48wing",                          # 炽天使之翼        [魔陷]
        "47lightning",                     # 雷霆裁决         [魔陷]
        "053dragons",                      # 三龙会议         [魔陷]
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
