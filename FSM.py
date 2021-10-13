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
                logging.debug(f"The screen has been refreshed! refreshScreenTime: {tool.formatTime(self.refreshScreenTime)}")

    def getCurrentStatus(self, refresh=True) -> Optional[Status]:
        if refresh:
            self.refreshScreen()
        logging.debug('Getting current status')
        curStatus = None
        for status in self.statusList:
            if status.check():
                curStatus = status 
                break
        logging.debug("Current status: {}".format(curStatus))
        return curStatus

    def beforeRun(self):
        self.nUnexpectedStatus = 0
        self.unexpectedStatus = None
        logging.debug(f"entering FSM {self.name}")

    def afterRun(self):
        logging.debug(f"leaving FSM {self.name}")

    def handleUnexpectedStatus(self, curStatus):
        if self.nUnexpectedStatus == self.unexpectedTolerance:
            logging.debug("got {} unexpected status: {}".format(self.nUnexpectedStatus, self.unexpectedStatus))
            return True
        elif self.unexpectedStatus == curStatus:
            self.nUnexpectedStatus += 1
        else:
            self.unexpectedStatus = curStatus
            self.nUnexpectedStatus = 0
        logging.debug(f"CurrentFSM: {self.name} got {self.nUnexpectedStatus} unexpected status: {self.unexpectedStatus}")
        return False

    def run(self, *args, **kwargs) :
        pass