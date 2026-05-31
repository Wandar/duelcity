# -*- coding: utf-8 -*-
import KBEngine
import gzip
import json
import random
import inspect
import importlib
import time
from KBEDebug import *
from globalvars import *
from a import CardBuff
import os
import importlib.util



"""
search all card Classes and debug card Classes from files

card Class must contain CARD_KEY
debug card Class must contain CARD_DATA
"""
_allkeys=[]
_allEffectNames=[]
debugDataList=[]

g_sourceCodes={} #cardKey:str

def mergeAllCards():
    g_allcardClass.clear()
    g_shortEffects.clear()
    _allkeys.clear()
    debugDataList.clear()
    _allEffectNames.clear()

    t1=time.time()
    _mergeCardsFolder("game_logic/cards_monster")
    _mergeCardsFolder("game_logic/cards_spelltrap")
    _mergeCardsModule("card_effects.debugCards")
    _mergeCardsModule("card_effects.shortEffects")
    INFO_MSG("merge all cards,used time=",time.time()-t1)

    recal_DEBUG_DATA_bytes()



def _mergeCardsFolder(folderPath):
    if not D_CARD or not len(D_CARD):
        ERROR_MSG("D_CARD not inited,check reloadData function")
        return

    if not os.path.isdir(folderPath):
        ERROR_MSG("mergeCardsFolder: folder not found:", folderPath)
        return

    for root, dirs, files in os.walk(folderPath):
        dirs.sort()  # 保证子文件夹遍历顺序一致
        for filename in sorted(files):
            if not filename.endswith('.py'):
                continue

            filepath = os.path.join(root, filename)
            module_name = filename[:-3]  # strip .py extension

            try:
                spec = importlib.util.spec_from_file_location(module_name, filepath)
                mo = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mo)
            except Exception as e:
                ERROR_MSG("mergeCardsFolder: failed to load file:", filepath, str(e))
                continue

            for name, Cls in inspect.getmembers(mo):
                ClsModuleName = getattr(Cls, "__module__", None)
                if not ClsModuleName:
                    continue
                if ClsModuleName != module_name:
                    continue  # skip imported classes (Card, Effect, etc.)

                card_key = getattr(Cls, 'CARD_KEY', None)
                if not card_key:
                    continue  # no CARD_KEY, skip

                if card_key.lower() in _allkeys:
                    ERROR_MSG("CARD_KEY duplication:%s" % card_key, Cls)
                    continue

                _allkeys.append(card_key.lower())
                g_allcardClass[card_key] = Cls



def _mergeCardsModule(moudleName):
    if not D_CARD or not len(D_CARD):
        ERROR_MSG("D_CARD not inited,check reloadData function")
        return

    mo=importlib.import_module(moudleName)
    for name,Cls in inspect.getmembers(mo): #include all import
        ClsModuleName=getattr(Cls,"__module__",None)
        if not ClsModuleName:
            continue
        if ClsModuleName  != moudleName:
            continue
        card_key=getattr(Cls,'CARD_KEY',None)
        if card_key:
            if card_key.lower() in _allkeys:
                ERROR_MSG("CARD_KEY duplication:%s"%card_key,Cls)
                continue
            else:
                _allkeys.append(card_key.lower())

            # if card_key not in D_CARD:
            #     # if not card_key.startswith("__"):
            #     ERROR_MSG("cant find CARD_KEY in ALL_DATA.json,CARD_KEY:",card_key)
            #     continue

            g_allcardClass[card_key]=Cls
        else:
            card_data=getattr(Cls,'CARD_DATA',None)
            if card_data:
                _tryMergeDebugCards(Cls,card_data)
            elif getattr(Cls,"__IS_EffectData__",None):
                if Cls.__name__ in _allEffectNames:
                    ERROR_MSG("duplicate Effect Class Name:",Cls.__name__)
                _allEffectNames.append(Cls.__name__)
                if getattr(Cls,"__IS_SHORT_EFFECT__",None):
                    g_shortEffects[Cls.__name__]=Cls



def _tryMergeDebugCards(Cls,card_data):
    isSuccess=_makeDebugCardData(card_data)
    if not isSuccess:
        return

    KEY=card_data["key"]

    if KEY.lower() in _allkeys:
        ERROR_MSG("KEY duplication:%s"%KEY,Cls)
        return
    else:
        _allkeys.append(KEY.lower())

    g_allcardClass[KEY]=Cls

    D_CARD[card_data["key"]]=card_data
    debugDataList.append(card_data)




def _makeDebugCardData(dataJson):
    if "key" not in dataJson:
        ERROR_MSG("card data error no key",dataJson)
        return False

    dataJson["debug"]=True

    key=dataJson["key"]

    for attrkey,v in D_CARD["version"].items():
        if attrkey not in dataJson:
            if type(v)==str:
                v=""
            elif type(v)==float:
                v=0.0
            elif type(v)==int:
                v=0
            elif type(v)==bool:
                v=False
            dataJson[attrkey]=v

    if dataJson["diameter"]<0.001:
        ERROR_MSG("you forget to set diameter:",key)
        dataJson["diameter"]=2

    for s in ("name_zh","name_en","name_ja","name_zh_tr"):
        if not dataJson[s]:
            dataJson[s]=dataJson["name_en"]

    for s in ("effect_zh","effect_en","effect_ja","effect_zh_tr"):
        if not dataJson[s]:
            dataJson[s]=dataJson["effect_en"]

    if "extradata" not in dataJson:
        dataJson["extradata"]={}
    return True



"""
compress debug card datas,send to client
"""
g_DEBUG_CARD_bytes=""
def recal_DEBUG_DATA_bytes():
    global g_DEBUG_CARD_bytes
    s=json.dumps(debugDataList)
    g_DEBUG_CARD_bytes=gzip.compress(s.encode(encoding="utf-8"))


################################BUFF
from Constants import CARD_BUFF
from a.CardBuff import g_buffClasses
def mergeCardBuff():
    mo=importlib.import_module("a.CardBuff")
    CardBuffBase=getattr(mo,"CardBuff")
    for name,value in CARD_BUFF.__dict__.items():
        if name.startswith("_"):
            continue
        if not isinstance(value,int):
            continue
        Cls=getattr(mo,name,None)
        if Cls is None or Cls is CardBuffBase or not getattr(Cls,"_IS_CARD_BUFF",None):
            Cls=type(name,(CardBuffBase,),{"BUFF_ID":value})
        else:
            Cls.BUFF_ID=value
        g_buffClasses[value]=Cls


from Constants import PLAYER_BUFF
from a.PlayerBuff import g_playerBuffClasses
def mergePlayerBuff():
    mo=importlib.import_module("a.PlayerBuff")
    PlayerBuffBase=getattr(mo,"PlayerBuff")
    for name,value in PLAYER_BUFF.__dict__.items():
        if name.startswith("_"):
            continue
        if not isinstance(value,int):
            continue
        Cls=getattr(mo,name,None)
        if Cls is None or Cls is PlayerBuffBase or not getattr(Cls,"_IS_PLAYER_BUFF",None):
            Cls=type(name,(PlayerBuffBase,),{"BUFF_ID":value})
        else:
            Cls.buffID=value
        g_playerBuffClasses[value]=Cls

#####################################