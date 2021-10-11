from enum import Enum
import logging


from FSM import FSM
from battleField import Direction
import tool
from card import Card, CardPlaceholder
from duel.status import *
from mystatus import getSaiStatus, inDiagLog
from general.status import generalStatusList
from login.status import loginPage
from login.fsm import LoginFSM
from homepage.status import homePage
from transportGateDuel.status import transportGateHomePage
from card import CardCollection
from battleField import BattleField, Direction
from unionForce.status import unionForcePage
from const import CARD_DICT_FILE
from connectionError.status import networkConnectionPage


class Phrase(Enum):
    DrawPharse = 0
    BattlePhrase = 1
    EndPhrase = 2

class BattleFSM(FSM):

    name = "BattleFSM"
    statusList = [
        manualDuelStatus
    ]
    
    def run(self):
        self.beforeRun()
        while True:
            curStatus = self.getCurrentStatus()
            if curStatus == manualDuelStatus:
                curStage = curStatus.getCurrentStage()
                if curStage == yourBattlePhraseIcon:
                    break
                elif curStatus.hasActionButton():
                    curStatus.transfer('showAction')
                elif curStatus.hasBattleButton():
                    curStatus.transfer('battle')
                else:
                    logging.debug("No proccessing for this")
            else:
                if self.handleUnexpectedStatus(curStatus):
                    break
        self.afterRun()
        return

class EndTurnFSM(FSM):

    name = "EndTurnFSM"

    statusList = [
        manualDuelStatus,
        duelFinishedPage
    ]
    

    def run(self):
        self.beforeRun()
        while True:
            curStatus = self.getCurrentStatus()
            if curStatus == manualDuelStatus:
                curStage = curStatus.getCurrentStage()
                if curStatus.hasActionButton():
                    curStatus.transfer('showAction')
                elif curStatus.hasEndTurnButton():
                    curStatus.transfer('endTurn')
                elif curStage == rivalPharseIcon: # finished ending turn
                    break
            elif curStatus == duelFinishedPage:
                break
            else:
                if self.handleUnexpectedStatus(curStatus):
                    break
        self.afterRun()
        return

def getCardArea(cardName, cardCollection):
    card = cardCollection.getCardByName(cardName)
    area = None
    if card.exists(init=True):
        area = card.area
    return area

def isCardInHandArea(*args, **kwargs):
    return getCardArea(*args, **kwargs) == 'hand'

def isCardInMonsterArea(*args, **kwargs):
    return getCardArea(*args, **kwargs) == 'monster'

def refreshScreen():
    FSM().refreshScreen()

def sumonCard(cardName, cardCollection):
    card = cardCollection.getCardByName(cardName)
    if card.exists(init=True):
        SumonFSM().run(card)
    refreshScreen()
    logging.debug(f"Monster {card} sumoned")

def attackCard(cardName, cardCollection, target=None):
    if isinstance(target, int):
        target = CardPlaceholder([(126, 244), (171, 168)])
    elif isinstance(target, str):
        target = cardCollection.getCardByName(target)
    card = cardCollection.getCardByName(cardName)
    if card.exists(init=True):
        AttackFSM().run(card, target=target)
    refreshScreen()

def useCard(cardName, cardCollection, target=None):
    if isinstance(target, int):
        target = CardPlaceholder([(27, 420), (120,557)])
    elif isinstance(target, str):
        target = cardCollection.getCardByName(target)
    card = cardCollection.getCardByName(cardName)
    if card.exists(init=True):
        UseFSM().run(card, target=target)
    logging.debug(f"Card {card} is used")
    refreshScreen()

def cardExists(cardName, cardCollection):
    card = cardCollection.getCardByName(cardName)
    return card.exists(init=True)

def testBattlePhrase(curStatus):
    logging.debug('testBattlePhrase start')
    bf = BattleField()
    cardCollection = CardCollection(CARD_DICT_FILE)
    isLastTurn = bf.nGetDeckLeftCard() == 0 or bf.nGetDeckLeftCard(direc=Direction.RIVAL) == 0
    logging.debug(f"LeftCard me: {bf.nGetDeckLeftCard()} rival: {bf.nGetDeckLeftCard(direc=Direction.RIVAL)}")
    if isLastTurn:
        dogCardName = '魔导兽 刻耳柏洛斯'
        monster2 = '不屈斗士 磊磊'
        monster3 = '守墓的随从'
        attackCard(monster3, cardCollection, 1)
    logging.debug('testBattlePhrase end')

def testMainPhrase(status):
    logging.debug('testMainPhrase end')
    nextPhrase = Phrase.EndPhrase
    bf = BattleField()
    cardCollection = CardCollection(CARD_DICT_FILE)
    dogCardName = '魔导兽 刻耳柏洛斯'
    monster2 = '不屈斗士 磊磊'
    monster3 = '守墓的随从'
    normalSpellCards = ['蓝药水', '行者哥布林', '火花', '天使的鲜血']

    # sumon monster
    isLastTurn = bf.nGetDeckLeftCard() == 0 or bf.nGetDeckLeftCard(direc=Direction.RIVAL) == 0
    logging.debug(f"LeftCard me: {bf.nGetDeckLeftCard()} rival: {bf.nGetDeckLeftCard(direc=Direction.RIVAL)}")
    if isCardInHandArea(dogCardName, cardCollection):
        sumonCard(dogCardName, cardCollection)
    else:
        if isLastTurn:
            if isCardInHandArea(monster3, cardCollection):
                sumonCard(monster3, cardCollection)
        else:
            if isCardInMonsterArea(dogCardName, cardCollection) and isCardInHandArea(monster2, cardCollection):
                sumonCard(monster2, cardCollection)
    if isCardInMonsterArea(dogCardName, cardCollection):
        for cardName in normalSpellCards:
            while isCardInHandArea(cardName, cardCollection):
                useCard(cardName, cardCollection)
    if isLastTurn:
        nextPhrase = Phrase.BattlePhrase
        for cardName in ['H-火热之心', '联合攻击']:
            while isCardInHandArea(cardName, cardCollection):
                if cardName == 'H-火热之心':
                    useCard('H-火热之心', cardCollection, target='魔导兽 刻耳柏洛斯')
                elif cardName == '联合攻击':
                    useCard('联合攻击', cardCollection, target='守墓的随从')
                else:
                    useCard(cardName, cardCollection)
    
    logging.debug('testMainPhrase end')
    return nextPhrase


class UseFSM(FSM):

    name = 'UseFSM'
    statusList = [
        manualDuelStatus,
        selectTargetPage
    ]
    

    def run(self, card, target=None):
        self.beforeRun()
        assert card.area == 'hand'
        used = False
        while True:
            curStatus = self.getCurrentStatus()
            if curStatus == manualDuelStatus:
                if used:
                    if manualDuelStatus.hasActionButton():
                        break
                    else:
                        logging.warning(f"Using card {card}")
                        manualDuelStatus.transfer("clickBlank")
                else:
                    if curStatus.hasButton('useCardButton'):
                        curStatus.transfer('useCard')
                        used =  True
                    else:
                        card.drag()
                        tool.sleep(0.5)
            elif curStatus == selectTargetPage:
                if curStatus.hasButton('confirmButton'):
                    curStatus.transfer('confirm')
                    break
                else:
                    curStatus.transfer('selectTargetByCard', args=(target,))
            else:
                if self.handleUnexpectedStatus(curStatus):
                    break
        self.afterRun()
        return


class SumonFSM(FSM):

    name = 'SumonFSM'

    statusList = [
        manualDuelStatus
    ]

    def run(self, card: Card):
        self.beforeRun()
        assert card.area == 'hand'
        sumoned = False
        while True:
            curStatus = self.getCurrentStatus()
            if curStatus == manualDuelStatus:
                if sumoned:
                    if manualDuelStatus.hasActionButton(): # sumon is finised
                        break
                    else:
                        logging.warning(f"Sumoning {card}")
                        manualDuelStatus.transfer('clickBlank')
                else:
                    if curStatus.hasButton('sumonButton'):
                        curStatus.transfer('sumon')
                        sumoned = True
                    else:
                        card.drag()
                        tool.sleep(0.5)
            else:
                if self.handleUnexpectedStatus(curStatus):
                    break
        self.afterRun()
        return

class AttackFSM(FSM):

    name = 'AttackFSM'
    statusList = [
        manualDuelStatus,
        duelFinishedPage
    ]
    def run(self, card, target=None):
        self.beforeRun()
        while True:
            curStatus = self.getCurrentStatus()
            card.init()
            if curStatus == manualDuelStatus:
                if card.exists():
                    card.drag(tool.get_center_point(target.position))
                    tool.sleep(0.2)
            elif curStatus == duelFinishedPage:
                break
            else:
                if self.handleUnexpectedStatus(curStatus):
                    break
        self.afterRun()
        return


class ManualDuelFSM(FSM):

    name = "ManualDuelFSM"

    statusList = [
        manualDuelStatus,
        useSkillPage,
        selectDuelMode,
        duelFinishedPage
    ]
    

    def run(self):
        self.beforeRun()
        while True:
            curStatus = self.getCurrentStatus()
            if  curStatus == selectDuelMode:
                curStatus.transfer('manualduel')
            elif curStatus == manualDuelStatus:
                curStage = curStatus.getCurrentStage()
                logging.debug(f"curStage: {curStage}")
                if curStatus.canUseSkill():
                    curStatus.transfer('clickUseSkillButton')
                elif curStage == yourDrawCardPhraseIcon:
                    logging.info('Waiting before drawCard')
                    tool.sleep(1)
                    curStatus.transfer('clickBlank')
                elif curStatus.isFirstTurn() or curStage == yourBattlePhraseIcon:
                    testBattlePhrase(curStatus)
                    EndTurnFSM().run()
                elif curStage == yourMainPhraseIcon:
                    nextPhrase = testMainPhrase(curStatus) 
                    if nextPhrase == Phrase.BattlePhrase:
                        BattleFSM().run()
                    elif nextPhrase == Phrase.EndPhrase:
                        EndTurnFSM().run()
                    else:
                        raise Exception(f"No such phrase {nextPhrase}")
            elif curStatus == useSkillPage:
                curStatus.transfer('useSkill')
            elif curStatus == duelFinishedPage:
                break
            else:
                if self.handleUnexpectedStatus(curStatus):
                    break
        self.afterRun()
        return None

class AutoDuelFSM(FSM):

    name = "AutoDuelFSM"
    statusList = [
        selectDuelMode, 
        inDuelStatus,
        duelFinishedPage
    ]
    

    def __init__(self) -> None:
        super().__init__()
        self.autoDualable = True

    def run(self):
        self.beforeRun()
        while True:
            curStatus = self.getCurrentStatus()
            if  curStatus == selectDuelMode:
                if not self.autoDualable or curStatus.leftZeroAutoDuel():
                    self.autoDualable = False
                    curStatus.transfer('return')
                else:
                    curStatus.transfer('autoDuel')
            elif curStatus == inDuelStatus:
                curStatus.transfer("wait")
            elif curStatus == duelFinishedPage:
                break
            else:
                if self.handleUnexpectedStatus(curStatus):
                    break
        self.afterRun()
        return self.autoDualable

class DuelFSM(FSM):

    statusList = [
        selectDuelMode,
        duelFinishedPage,
        duelResultsPage,
        getSaiStatus,
        loginPage,
        inDuelStatus,
        inDiagLog,
        transportGateHomePage,
        homePage,
        unionForcePage, 
        networkConnectionPage
    ] + generalStatusList

    name = 'DuelFSM'

    def __init__(self) -> None:
        super().__init__()
        self.autoDuelable = None

    def run(self, duelFSM=AutoDuelFSM()):
        self.beforeRun()
        self.isWin = None
        while True:
            curStatus = self.getCurrentStatus()
            if  curStatus == selectDuelMode:
                self.ableDuelable = duelFSM.run()
            elif curStatus == duelFinishedPage:
                self.isWin = curStatus.isWin()
                curStatus.transfer("yes")
            elif curStatus == duelResultsPage:
                if curStatus.hasButton('next'):
                    curStatus.transfer("next")
                elif curStatus.hasButton('yes'):
                    curStatus.transfer('yes')
                else:
                    curStatus.transfer("randomClick")
            elif curStatus in generalStatusList:
                curStatus.transfer("default")
            elif curStatus == loginPage:
                LoginFSM().run()
            elif curStatus == networkConnectionPage:
                networkConnectionPage.transfer("retry")
            elif curStatus in {transportGateHomePage, homePage, inDiagLog, unionForcePage}:
                break
            else:
                if self.handleUnexpectedStatus(curStatus):
                    break
        self.afterRun()
        return self.autoDuelable
