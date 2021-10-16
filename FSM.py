import tool
from typing import Optional
import numpy as np
import logging
import time
import mystatus
from mystatus import Status
from log.log import setupLogging
from const import MIN_REFRESH_INTERVAL, FSM_UNEXPECTED_TOLERANCE

setupLogging()

class FsmMetaClass(type):
    def __init__(cls, *args, **kwargs):
        cls.statusList.sort(key=lambda status: status.level, reverse=True)
    
class FSM(metaclass=FsmMetaClass):

    statusList =  []
    refreshScreenTime = -1
    minRefreshInterval = MIN_REFRESH_INTERVAL
    unexpectedTolerance = FSM_UNEXPECTED_TOLERANCE
    name = 'FSM'

    def __init__(self) -> None:
        self.lastUnexpectedOccurTime = -1

    def showScreen(self):
        tool.imshow(tool.get_appshot())

    def refreshScreen(self):
        """
        Control refresh frequency
        """
        now = time.time()
        interval = now - max(mystatus.lastClickTime, self.refreshScreenTime)
        if interval < self.minRefreshInterval:
                sleepTime = np.round(self.minRefreshInterval - interval, 3)
                logging.info(f"Refresh screen too frequently! Sleep for {sleepTime}s")
                time.sleep(sleepTime)
                self.refreshScreen()
        else:
                self.refreshScreenTime = time.time()
                tool.capture_screenshot()
                logging.info(f"The screen has been refreshed! refreshScreenTime: {tool.formatTime(self.refreshScreenTime)}")

    def getCurrentStatus(self, refresh=True) -> Optional[Status]:
        if refresh:
            self.refreshScreen()
        logging.info(f'{self.name}: Getting current status')
        curStatus = None
        for status in self.statusList:
            if status.check():
                curStatus = status 
                break
        logging.info(f"{self.name}: Current status: {curStatus}")
        return curStatus

    def beforeRun(self):
        self.nUnexpectedStatus = 0
        self.unexpectedStatus = None
        logging.info(f"entering FSM {self.name}")

    def afterRun(self):
        logging.info(f"leaving FSM {self.name}")

    def handleUnexpectedStatus(self, curStatus):
        now = time.time()
        if self.nUnexpectedStatus == self.unexpectedTolerance:
            logging.info("got {} unexpected status: {}".format(self.nUnexpectedStatus, self.unexpectedStatus))
            return True
        elif self.unexpectedStatus == curStatus and (self.lastUnexpectedOccurTime == -1 or (now - self.lastUnexpectedOccurTime) < 10):
            self.nUnexpectedStatus += 1
            logging.info(f"CurrentFSM: {self.name} got {self.nUnexpectedStatus} unexpected status: {self.unexpectedStatus}")
        else:
            self.lastUnexpectedOccurTime = now
            self.unexpectedStatus = curStatus
            self.nUnexpectedStatus = 0
            logging.info(f"Reset unexpected status!")
        return False

    def run(self, *args, **kwargs) :
        pass