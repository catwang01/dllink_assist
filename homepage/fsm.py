import logging
import random
import time


import tool
from FSM import FSM
from general.status import generalStatusList 
from login.status import loginPage
from login.fsm import LoginFSM
from homepage.status import *
from activity.sai.status import saiHomePage
from activity.sai.fsm import SaiFSM
from activity.ddCastle.fsm import DDCastleFSM
from activity.ddCastle.status import ddCastleHomePage
from unionForce.fsm import UnionForceFSM
from unionForce.status import unionForcePage
from tool import capitalize
from transportGateDuel.fsm import TransportGateFSM
from transportGateDuel.status import transportGateHomePage
from duel.fsm import AutoDuelFSM, DuelFSM, ManualDuelFSM
from duel.status import selectDuelMode
from maze.status import inMazeStatus
from maze.fsm import MazeFSM
from mystatus import inDiagLog, getSaiStatus
from log.log import setupLogging

setupLogging()

class CollectKeysInCurrentChannel(FSM):

    name = 'CollectKeysInOneChannel'
    statusList = [homePage] + generalStatusList

    def run(self):
        self.beforeRun()
        nCollected = 0
        while True:
            curStatus = self.getCurrentStatus()
            if curStatus == homePage:
                nKeys = curStatus.countKeys()
                logging.info("Find {} keys in current channel".format(nKeys))
                if nKeys > 0:
                    curStatus.transfer('collectOneKey')
                    nCollected += 1
                else:
                    break
            elif curStatus in generalStatusList:
                curStatus.transfer('default')
            else:
                if self.handleUnexpectedStatus(curStatus):
                    break
        self.afterRun()
        return nCollected

class CollectHiddentItemFSM(FSM):

    name = 'CollectHiddentItemFSM'
    statusList = [homePage] + generalStatusList

    def run(self):
        self.beforeRun()
        pointDict = {
            'DM': {
            'monsterGate': [41, 300],
            'transportGate': [225, 326],
            'workshop': [138, 540],
            'store': [225, 275],
            'pvp': [66, 430]
        }, 'GX': {
            'monsterGate': [41, 300],
            'transportGate': [225, 326],
            'workshop': [130, 558],
            'store': [225, 275],
            'pvp': [144, 423] 
        }
        } 
        clicked = False
        while True:
            curStatus = self.getCurrentStatus()
            if curStatus == homePage:
                if not clicked:
                    channel = homePage.inWhichChannel()
                    world = homePage.getCurrentWorld()
                    homePage.transfer('click', 2, args=(pointDict[world][channel],))
                    clicked = True
                else:
                    break
            elif curStatus in generalStatusList:
                curStatus.transfer('default')
            else:
                if self.handleUnexpectedStatus(curStatus):
                    break
        self.afterRun()
        return


class TransferAllChannels(FSM):

    name = 'TransferAllChannels'
    statusList = [
        homePage
    ] + generalStatusList

    def run(self, fsm, *args, **kwargs):
        self.beforeRun()
        channels = ['pvp', 'transportGate', 'store', 'workshop', 'monsterGate']
        while True:
            curStatus = self.getCurrentStatus()
            if curStatus == homePage:
                if len(channels) == 0:
                    break
                while len(channels):
                    curStatus = self.getCurrentStatus()
                    if curStatus == homePage:
                        channel = random.choice(channels)
                        SwitchChannelFSM().run(channel)
                        ret = fsm.run(*args, **kwargs)
                        channels.remove(channel)
                        yield channel, ret
                    elif curStatus in generalStatusList:
                        curStatus.transfer('default')
                    elif curStatus == someoneAppearIcon:
                        curStatus.transfer('know')
                    else:
                        break
            elif curStatus in generalStatusList:
                curStatus.transfer('default')
            elif curStatus == someoneAppearIcon:
                curStatus.transfer('iknow')
            else:
                if self.handleUnexpectedStatus(curStatus):
                    break
        self.afterRun()
        return


class DuelWithAllNpcInCurrentChannel(FSM):

    name = 'DuelWithAllNpcInCurrentChannel'
    statusList = [homePage, inDiagLog, selectDuelMode] + generalStatusList

    def run(self):
        self.beforeRun()
        nNormalNpcs = 0
        while True:
            curStatus = self.getCurrentStatus()
            if curStatus == homePage:
                if curStatus.countNormalNpcs():
                    curStatus.transfer('clickOneNormalNpc', 2)
                else:
                    break
            elif curStatus in {inDiagLog, selectDuelMode}:
                DuelWithOneNormalNPC().run()
                nNormalNpcs += 1
            elif curStatus in generalStatusList:
                curStatus.transfer('default')
            else:
                if self.handleUnexpectedStatus(curStatus):
                    break
        self.afterRun()
        return nNormalNpcs


class DuelWithOneNormalNPC(FSM):

    name = 'DuelWithOneNormalNPC'
    statusList = [
        inDiagLog,
        selectDuelMode,
        loginPage,
        homePage
    ] + generalStatusList

    def run(self):
        self.beforeRun()
        nDiagLog = 0
        isWin = None
        while True:
            curStatus = self.getCurrentStatus()
            if curStatus == homePage:
                if nDiagLog >= 2:
                    print(f"Duel finished! Result: {'Won' if isWin else 'Lost'}")
                else:
                    print('Homepage! Not Duel screen! Returned!')
                break
            elif curStatus == inDiagLog:
                curStatus.transfer('next', 5)
                nDiagLog += 1
            elif curStatus == selectDuelMode:
                autoDuelable, isWin = DuelFSM().run()
            elif curStatus in generalStatusList:
                curStatus.transfer("default")
            elif curStatus == loginPage:
                LoginFSM().run()
            else:
                if self.handleUnexpectedStatus(curStatus):
                    break
        self.afterRun()
        return

class SwitchChannelFSM(FSM):

    name = 'SwitchChannelFSM'
    statusList = [
        homePage
    ]

    def run(self, channel):
        self.beforeRun()
        logging.debug("goto {}".format(channel))
        while True:
            curStatus = self.getCurrentStatus()
            if curStatus == homePage:
                currentChannel = curStatus.inWhichChannel()
                logging.debug("current: {} goto: {}".format(currentChannel, channel))
                if  currentChannel != channel:
                    curStatus.transfer('select{}'.format(capitalize(channel)), 5)
                else:
                    logging.debug("Staying current channel")
                    break
            else:
                if self.handleUnexpectedStatus(curStatus):
                    break
        self.afterRun()
        return

class HomepageEnterUnionForce(FSM):

    name = 'HomepageEnterUnionForce'
    statusList = [homePage, unionForcePage]

    def run(self):
        self.beforeRun()
        canContinue = True
        while True:
            curStatus = self.getCurrentStatus()
            if curStatus == homePage:
                if canContinue:
                    if curStatus.hasButton('unionForceIcon'):
                        curStatus.transfer('enterUionForce')
                    else:
                        SwitchChannelFSM().run('pvp')
                else:
                    break
            elif curStatus == unionForcePage:
                canContinue = UnionForceFSM().run()
            else:
                if self.handleUnexpectedStatus(curStatus):
                    break
        self.afterRun()
        return 

class HomepageEnterDDCastle(FSM):
    
    name = 'HomepageEnterDDCastle'
    statusList = [homePage, ddCastleHomePage] + generalStatusList

    def run(self):
        self.beforeRun()
        while True:
            curStatus = self.getCurrentStatus()
            if curStatus == homePage:
                if curStatus.hasButton('ddCastleIcon'):
                    curStatus.transfer('enterDDCastle')
            elif curStatus == ddCastleHomePage:
                DDCastleFSM().run()
            elif curStatus in generalStatusList:
                curStatus.transfer('default')
            elif curStatus == someoneAppearIcon:
                curStatus.transfer("iknow")
            else:
                if self.handleUnexpectedStatus(curStatus):
                    break
        self.afterRun()
        return

class HomePageFSM(FSM):

    name = 'HomePageFSM'
    statusList = [
        homePage,
        inDiagLog,
        selectDuelMode,
        getSaiStatus,
        switchingWorldStatus,
        loginPage,
        inMazeStatus,
        saiHomePage,
        transportGateHomePage
    ] + generalStatusList

    def initRun(self):
        self.unexpectedStatus = None
        self.nUnexpectedStatus = 0

    def changeWorld(self, targetWorld=None):
        self.initRun()
        logging.debug("entering changeWorld")
        while True:
            curStatus = self.getCurrentStatus()
            if curStatus == homePage:
                curStatus.transfer("switchWorld")
            elif curStatus == switchingWorldStatus:
                if targetWorld is None or targetWorld == "DMWorld":
                    curStatus.transfer('switchToDMWorld', 3)
                else:
                    curStatus.transfer('switchToGXWorld', 3)
                logging.debug("Goto world: {}".format(targetWorld))
                break
            else:
                if self.handleUnexpectedStatus(curStatus):
                    break
        logging.debug("leaving changeWorld")
        return

    def runSai(self):
        self.initRun()
        logging.debug("entering runSai")
        while True:
            curStatus = self.getCurrentStatus()
            if curStatus == homePage:
                curStatus.transfer("gotoSaiHomePage", 3)
            elif curStatus == saiHomePage:
                SaiFSM().run()
                break
            else:
                if self.handleUnexpectedStatus(curStatus):
                    break
        logging.debug('leaving runSai!')
        return

    def runMaze(self):
        self.initRun()
        logging.debug("entering runMaze")
        while True:
            curStatus = self.getCurrentStatus()
            if curStatus == inMazeStatus:
                MazeFSM().run()
                break
            else:
                if self.handleUnexpectedStatus(curStatus):
                    break
        logging.debug("starting runMaze")
        return

    def transportGateDuel(self, roleName='yukijudai', level=10, duelFSM=None):
        if duelFSM is None:
            duelFSM = AutoDuelFSM()
        self.initRun()
        logging.debug('entering transportGateDuel!')
        while True:
            curStatus = self.getCurrentStatus()
            if curStatus == homePage:
                currentChannel = curStatus.inWhichChannel()
                if currentChannel == 'transportGate':
                    curStatus.transfer('enterTransportGate')
                else:
                    curStatus.transfer('selectTransportGate')
            elif curStatus == transportGateHomePage:
                    TransportGateFSM().run(roleName, 'level{}'.format(level), duelFSM)
                    break
            elif curStatus in generalStatusList:
                curStatus.transfer("default")
            else:
                if self.handleUnexpectedStatus(curStatus):
                    break
        logging.debug('leaving transportGateDuel!')
        return

    def collectKeys(self):
        results = TransferAllChannels().run(CollectKeysInCurrentChannel())
        for ret, channel in results:
            pass

    def duelWithNormalNpcs(self):
        results = TransferAllChannels().run(DuelWithAllNpcInCurrentChannel())
        for ret, channel in results:
            pass

    def collectHiddenItems(self):
        results = TransferAllChannels().run(CollectHiddentItemFSM())
        for ret, channel in results:
            pass

    def unionForceChallenge(self):
        HomepageEnterUnionForce().run()

    def runDDCastle(self):
        HomepageEnterDDCastle().run()

    def run(self):
        for world in ['DMWorld', 'GXWorld']:
            self.changeWorld(world)
            tool.sleep(3)
            self.collectKeys()
            tool.sleep(3)
            self.duelWithNormalNpcs()
            tool.sleep(3)
            # self.runDDCastle()
            # tool.sleep(3)
            self.unionForceChallenge()
            tool.sleep(3)
            self.collectHiddenItems()
            # tool.sleep(3)
            # self.runSai()
            # for i in range(10):
            #     # tianjoyin
            #     # yukijudai
            #     # mutouyougi
            #     self.transportGateDuel(roleName='yukijudai', duelFSM=ManualDuelFSM())
            #     tool.sleep(3)