import logging
import random
import time


from FSM import FSM
from general.status import generalStatusList 
from login.status import loginPage
from login.fsm import LoginFSM
from homepage.status import *
from activity.sai.status import saiHomePage
from activity.sai.fsm import SaiFSM
from tool import capitalize
from transportGateDuel.fsm import TransportGateFSM
from transportGateDuel.status import transportGateHomePage
from duel.fsm import DuelFSM
from duel.status import selectDuelMode
from maze.status import inMazeStatus
from maze.fsm import MazeFSM
from mystatus import inDiagLog, getSaiStatus
from log.log import setupLogging

setupLogging()

class CollectKeyFSM(FSM):

    statusList = [
        homePage
    ] + generalStatusList
    statusList.sort(key=lambda status: status.level, reverse=True)

    name = "CollectKeyFSM"

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
                break
        self.afterRun()
        return nCollected

class HomePageFSM(FSM):

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
    statusList.sort(key=lambda x: x.level, reverse=True)

    def initRun(self):
        self.unexpectedStatus = None
        self.nUnexpectedStatus = 0

    def changeWorld(self, targetWorld=None):
        self.initRun()
        logging.debug("entering changeWorld")
        while True:
            curStatus = self.getCurrentStatus()
            if curStatus == homePage:
                curStatus.transfer("switchWorld", 1)
            elif curStatus == switchingWorldStatus:
                if targetWorld is None or targetWorld == "DMWorld":
                    curStatus.transfer('switchToDMWorld', 5)
                else:
                    curStatus.transfer('switchToGXWorld', 5)
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

    def collectKeys(self):
        self.initRun()
        logging.debug("entering collectKeys")
        while True:
            curStatus = self.getCurrentStatus()
            if curStatus == homePage:
                channels = ['pvp', 'transportGate', 'store', 'workshop', 'monsterGate']
                nChannels = len(channels)
                logging.info("Collecting keys...")
                startTime = time.time()
                nTotalCollected = 0
                while len(channels):
                    if curStatus == homePage:
                        channel = random.choice(channels)
                        logging.debug("goto {}".format(channel))
                        currentChannel = curStatus.inWhichChannel()
                        nCollected = CollectKeyFSM().run()
                        logging.debug("current: {} goto: {}".format(currentChannel, channel))
                        if  currentChannel != channel:
                            curStatus.transfer('select{}'.format(capitalize(channel)))
                        else:
                            logging.debug("Staying current channel")
                        logging.info(f"Collecting keys in channel {channel}")

                        logging.info(f"Collected {nCollected} keys in current channel: {channel}")
                        channels.remove(channel)
                        logging.info(f"Total channels: {nChannels} Collected: {nChannels - len(channels)} Left: {len(channels)}")
                        nTotalCollected += nCollected 
                    else:
                        break
                endTime = time.time()
                logging.info("Collecting finished! TimeUsed: {}s Total collected keys: {}".format(int(endTime - startTime), nTotalCollected))
                break
            elif curStatus in generalStatusList:
                curStatus.transfer('default')
            else:
                if self.handleUnexpectedStatus(curStatus):
                    break
        logging.debug("leaving collectKeys")
        return

    def duelWithOneNormalNpc(self):
        self.initRun()
        logging.debug('entering duelWithOneNormalNpc')
        nDiagLog = 0
        isWin = None
        while True:
            curStatus = self.getCurrentStatus()
            if curStatus == inDiagLog:
                curStatus.transfer('next', 5)
                nDiagLog += 1
            elif curStatus == selectDuelMode:
                DuelFSM().run()
            elif curStatus in generalStatusList:
                curStatus.transfer("default")
            elif curStatus == loginPage:
                LoginFSM().run()
            elif curStatus == homePage:
                if nDiagLog >= 2:
                    print(f"Duel finished! Result: {'Won' if isWin else 'Lost'}")
                else:
                    print('Homepage! Not Duel screen! Returned!')
                break
            else:
                if self.handleUnexpectedStatus(curStatus):
                    break
        logging.debug('leaving duelWithOneNormalNpc')
        return


    def duelWithNormalNpcs(self):
        self.initRun()
        logging.debug("entering duelWithNormalNpcs")
        while True:
            curStatus = self.getCurrentStatus()
            if curStatus == homePage:
                channels = ['pvp', 'transportGate', 'store', 'workshop', 'monsterGate']
                nChannels = len(channels)
                logging.info("Searching normal npcs...")
                startTime = time.time()
                nTotalSearched = 0
                while len(channels):
                    channel = random.choice(channels)
                    nSearched = 0
                    logging.debug("goto {}".format(channel))
                    currentChannel = curStatus.inWhichChannel()
                    logging.debug("current: {} goto: {}".format(currentChannel, channel))
                    if  currentChannel != channel:
                        curStatus.transfer('select{}'.format(capitalize(channel)), 5)
                    else:
                        logging.debug("Staying current channel")
                    logging.info("Searching normal npcs in {}".format(channel))
                    while True:
                        curStatus = self.getCurrentStatus()
                        if curStatus == homePage:
                            nNpcs = curStatus.countNormalNpcs()
                            if nNpcs > 0:
                                logging.info("Find {} normal npcs in current channel".format(nNpcs))
                                curStatus.transfer('clickOneNormalNpc')
                                self.duelWithOneNormalNpc()
                                nSearched += 1
                            else:
                                logging.info("Find no normal npcs in current channel!".format(nNpcs))
                                break
                        elif curStatus == inDiagLog:
                            curStatus.transfer('next')
                        elif curStatus in generalStatusList:
                            curStatus.transfer('default')
                        else:
                            return 
                    logging.info("Searched {} normal npcs in current channel: {}".format(nSearched, channel))
                    channels.remove(channel)
                    logging.info("Total channels: {} Searched: {} Left: {}".format(nChannels, nChannels - len(channels), len(channels)))
                    nTotalSearched += nSearched 
                endTime = time.time()
                logging.info("Searching finished! TimeUsed: {}s Total search normal npcs: {}".format(int(endTime - startTime), nTotalSearched))
                break
            else:
                if self.handleUnexpectedStatus(curStatus):
                    break
        logging.debug("leaving duelWithNormalNpcs")
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

    def transportGateDuel(self, roleName='yukijudai', level=10):
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
                    TransportGateFSM().run(roleName, 'level{}'.format(level))
                    break
            elif curStatus in generalStatusList:
                curStatus.transfer("default")
            else:
                if self.handleUnexpectedStatus(curStatus):
                    break
        logging.debug('leaving transportGateDuel!')
        return

    def run(self):
        for world in ['DMWorld', 'GXWorld']:
            self.changeWorld(world)
            time.sleep(3)
            self.collectKeys()
            time.sleep(3)
            self.duelWithNormalNpcs()
            time.sleep(3)
            # self.runSai()
            # time.sleep(3)
            # self.transportGateDuel(roleName='tianjoyin')
