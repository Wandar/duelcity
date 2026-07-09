# -*- coding: utf-8 -*-
from __future__ import annotations

from util import *
from annos import *
from a.DuelConstants import *
from decks import decks
from KBEngine import *

# Re-exports: external code imports these from duelbot.botPack1
# (AvatarBA / AvatarCE / annos), keep the paths stable.
from duelbot.aiBase import DuelAIBase, AI_MSG
from duelbot.aiBrain import DuelAINormal, DuelAI_dragon

"""
================================================================================
Duel AI package overview  (see design/duelbot_ai_design.md)
================================================================================
This file: bot configs (MENU_BOTS) + re-exports only. The AI itself:

  aiBase.py    engine plumbing + main loop (repeat y_think until done)
  aiBrain.py   DuelAINormal.y_think() — ALL strategy in one if/else; each
               branch probes a y_ helper with justCheck=True, then runs it
  aiCombos.py  combo functions y_combo_xxx(bot, justCheck) + COMBOS registry
  aiSupply.py  CardSupply — hidden-card morphing (never create-on-field)
  aiChoice.py  popup / card-selector answering policy

Core design:
  - The account-side win/lose pool decides self.shouldWin per duel; every
    decision keys off it (go first when winning, cancel selectors when
    losing, mercy in battle, signature-monster script, ...).
  - The bot plays REAL hand cards whenever possible. When it needs a card it
    doesn't have, the CardSupply rewrites the identity of a hand/deck card
    the player has never seen (hand = card back, deck = count only), then the
    card is played through the normal flow, indistinguishable from a real draw.
  - Combos: config lists combo names; each is one function in aiCombos.py.
    Missing cards are morphed into the hand first, then the combo runs.

MENU_BOTS config keys:
  funTurns          turns at duel start with small monsters only
  preferCards       deck-flavored cardKeys (LV<=4 ones become the small pool;
                    duplicates act as weights)
  signatureMonsters big signature cardKeys (empty -> global high-level pool)
  signatureTurn     earliest turn (randomized +-) for the signature script
  combos            combo names from aiCombos.COMBOS, priority = list order
================================================================================
"""

MENU_BOTS = {
    TESTPLAY_BOT: {
        "avatarKey": "yblack",
        "picture": "",
        "title": "",
        "description": "",
        "aiClass": DuelAINormal,
        "deck": decks.DEBUG_DECK1,
        "preferScene": DEBUG_SCENE,
        "funTurns": 3,
        "signatureMonsters": [],   # empty -> global high-level pool
        "combos": [],
    },
    "tutorialBot": {
        "avatarKey": "whitetail",
        "picture": "",
        "title": "",
        "description": "",
        "aiClass": DuelAINormal,
        "deck": decks.DEBUG_DECK1,
        "preferScene": "cc/factory_parking/factory_parking",
        "funTurns": 99,            # small monsters forever
        "signatureMonsters": [],
        "combos": [],
    },
    "bot1": {
        "avatarKey": "yblack",
        "picture": "Clash for Supremacy",
        "title": "Clash for Supremacy",
        "description": "",
        "aiClass": DuelAINormal,
        "deck": decks.DEBUG_DECK1,
        "preferRace": RACE.DRAGON,
        "preferCards": [
            "ToonDragon_Lowpoly", "cartoonDragon", "cartoonLeviathan", "cartoonWyvern",
            "SK_BabyDragon", "Dragon Inferno", "FireDragonRed", "ForestDrake_Blue",
            "smallDragonWhelp_Rd", "Fantasy Dragon-Blue", "Drake Skinny",
        ],
        "preferScene": "cc/modular_town/modular_town",
        "funTurns": 3,
        "signatureMonsters": [
            "MountainDragon", "cartoonChineseDragon", "Wyrm1_2", "Wyvern", "dragonrex",
        ],
        "combos": ["dragonRush"],
    },
    "bot2": {
        "avatarKey": "greentrenchcoatman",
        "picture": "Abyssal Sea Hunting Grounds",
        "title": "Abyssal Sea Hunting Grounds",
        "description": "",
        "aiClass": DuelAINormal,
        "deck": decks.DEBUG_DECK1,
        "preferRace": RACE.AQUA,
        "preferCards": [
            "Bass_LOD0", "CrabMonsterDefault", "Catfish_LOD0", "giantcrab",
            "weranglerfish", "SKM_whale", "Walrus_LOD0", "SeaLion_LOD0", "StoneBeast",
        ],
        "preferScene": "cc/topdownforest/topdownforest",
        "funTurns": 3,
        "signatureMonsters": [
            "werecrab", "Voidray", "toon_Lobster", "SKM_squid", "Turtle_Blue_Shell_01",
        ],
        "combos": [],
    },
    "bot3": {
        "avatarKey": "greentrenchcoatman",
        "picture": "Carapace Vanguard",
        "title": "Carapace Vanguard",
        "description": "",
        "aiClass": DuelAINormal,
        "deck": decks.DEBUG_DECK1,
        "preferRace": RACE.INSECT,
        "preferCards": [
            "ms03_Bee_1", "Wasp_Blue", "Caterpillar", "JapaneseHornet",
            "Ladybug", "Mantis", "Moth", "Beast_1",
        ],
        "preferScene": "cc/luna_park/luna_park",
        "funTurns": 3,
        "signatureMonsters": [
            "GiantBeetle", "RhinocerosBeetle",
        ],
        "combos": [],
    },
    "bot4": {
        "avatarKey": "whitehairman",
        "picture": "Claw of the Verdant Wilds",
        "title": "Claw of the Verdant Wilds",
        "description": "",
        "aiClass": DuelAINormal,
        "deck": decks.DEBUG_DECK1,
        "preferRace": RACE.PLANT,
        "preferCards": [
            "StumpEnt_Autumn", "Sun Blossom", "Spore", "ms02_Stump_1",
            "Cactus Boss", "Sunflower Fairy", "Ent", "Treant_Summer",
            "Plant Chewer", "TreantGuard-Green",
        ],
        "preferScene": "cc/summer_beach/summer_beach",
        "funTurns": 3,
        "signatureMonsters": [
            "Sunflora Pixie",
        ],
        "combos": [],
    },
    "bot5": {
        "avatarKey": "glassredcoat",
        "picture": "Crimson Flame Tide",
        "title": "Crimson Flame Tide",
        "description": "",
        "aiClass": DuelAINormal,
        "deck": decks.DEBUG_DECK1,
        "preferRace": RACE.DRAGON,
        "preferCards": [
            "ToonDragon_Lowpoly", "cartoonDragon", "cartoonLeviathan", "cartoonWyvern",
            "SK_BabyDragon", "Dragon Inferno", "FireDragonRed", "ForestDrake_Blue",
            "smallDragonWhelp_Rd", "Fantasy Dragon-Blue", "Drake Skinny",
        ],
        "preferScene": "cc/topdownforest/topdownforest",
        "funTurns": 3,
        "signatureMonsters": [
            "desertdragon", "Wyrm1_2", "plainsdragon", "polardragon", "dragonrex",
        ],
        "combos": [],
    },
    "bot6": {
        "avatarKey": "brownvest",
        "picture": "Forest Little Rascal",
        "title": "Forest Little Rascal",
        "description": "",
        "aiClass": DuelAINormal,
        "deck": decks.DEBUG_DECK1,
        "preferRace": RACE.BEASTWARRIOR,
        "preferCards": [
            "OrcPBR", "ms06_Rat_1", "ms04_01_Minotaur_2", "RatAssassinDefault",
            "WerewolfMaskTint", "Kitsune_2", "Dragonide",
        ],
        "preferScene": "cc/factory_parking/factory_parking",
        "funTurns": 3,
        "signatureMonsters": [
            "Dog Bowwow", "SwordsTiger",
        ],
        "combos": [],
    },
    "bot7": {
        "avatarKey": "whitetail",
        "picture": "Growth Element",
        "title": "Growth Element",
        "description": "",
        "aiClass": DuelAINormal,
        "deck": decks.DEBUG_DECK1,
        "preferRace": RACE.FAIRY,
        "preferCards": [
            "Whirlwind", "tinyWind", "Lyme",
        ],
        "preferScene": "cc/modular_town/modular_town",
        "funTurns": 3,
        "signatureMonsters": [
            "Wind Mage", "cartoonKitsune",
        ],
        "combos": [],
    },
    "bot8": {
        "avatarKey": "Tangsuithoodieman",
        "picture": "Jurassic Rallying Call",
        "title": "Jurassic Rallying Call",
        "description": "",
        "aiClass": DuelAINormal,
        "deck": decks.DEBUG_DECK1,
        "preferRace": RACE.DINOSAUR,
        "preferCards": [
            "Pterodactyl", "Mosasaurus", "Triceratops", "Ankylosaurus",
            "Pachycephalosaurus", "Stegosaurus", "T Rex", "Brachiosaurus",
            "Dilophosaurus", "Parasaurolophus",
        ],
        "preferScene": "cc/summer_beach/summer_beach",
        "funTurns": 3,
        "signatureMonsters": [],   # empty -> global high-level pool
        "combos": [],
    },
    "bot9": {
        "avatarKey": "bwmaidoutfit",
        "picture": "Woodland Cuties",
        "title": "Woodland Cuties",
        "description": "",
        "aiClass": DuelAINormal,
        "deck": decks.DEBUG_DECK1,
        "preferRace": RACE.BEAST,
        "preferCards": [
            "Dino_Cat_04", "Cat Bolt", "Cat Lightning", "cartoonPegasus", "Goat_LOD0",
            "Werewolf", "Dog Bark", "ThreeTailedWolf", "toon_RedPanda",
            "toon_SnappingTurtle", "Lynx_LOD0", "Llama_LOD0",
        ],
        "preferScene": "cc/sacred_desert/sacred_desert",
        "funTurns": 3,
        "signatureMonsters": [
            "toon_Crocodile", "toon_Hedgehog", "toon_Skunk", "Moose_LOD0",
            "Unicorn_Pegasus", "cartoonCerberus", "cartoonKirin", "GhostTiger",
        ],
        "combos": [],
    },
}
