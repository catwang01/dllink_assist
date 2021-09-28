import tool
from typing import Optional
import numpy as np
import logging
import time
import mystatus
from mystatus import Status
from log.log import setupLogging

setupLogging()

class FSM:

    statusList =  []
    refreshScreenTime = -1
    minRefreshInterval = 1
    name = 'FSM'

    def showScreen(self):
        tool.showImg(tool.get_appshot())

    def refreshScreen(self):
        """
        Control refresh frequency
        """
        now = time.time()
        interval = now - max(mystatus.lastClickTime, self.refreshScreenTime)
        logging.debug("laskClickTime: {}, self.refreshScreenTime: {} now: {}".format(mystatus.lastClickTime, self.refreshScreenTime, now))
        if interval < self.minRefreshInterval:
                sleepTime = np.ceil(self.minRefreshInterval - interval)
                logging.info("Refresh screen too frequently! Sleep for {}s".format(sleepTime))
                time.sleep(sleepTime)
                self.refreshScreen()
        else:
                self.refreshScreenTime = time.time()
                tool.capture_screenshot()
                logging.debug("The screen has been refreshed! refreshScreenTime: {}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.refreshScreenTime))))

    def showScreen(self):
        tool.showImg(tool.get_appshot())

    def refreshScreen(self):
        """
        Control refresh frequency
        """

        now = time.time()
        interval = now - max(mystatus.lastClickTime, self.refreshScreenTime)
        logging.debug("laskClickTime: {}, self.refreshScreenTime: {} now: {}".format(mystatus.lastClickTime, self.refreshScreenTime, now))
        if interval < self.minRefreshInterval:
            sleepTime = np.ceil(self.minRefreshInterval - interval)
            logging.info("Refresh screen too frequently! Sleep for {}s".format(sleepTime))
            time.sleep(sleepTime)
            self.refreshScreen()
        else:
            self.refreshScreenTime = time.time()
            tool.capture_screenshot()
            logging.debug("The screen has been refreshed! refreshScreenTime: {}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.refreshScreenTime))))

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
        logging.debug(f"entering {self.name}")

    def afterRun(self):
        logging.debug(f"leaving {self.name}")

    def handleUnexpectedStatus(self, curStatus):
        if self.nUnexpectedStatus == 20:
            logging.debug("got {} unexpected status: {}".format(self.nUnexpectedStatus, self.unexpectedStatus))
            return True
        elif self.unexpectedStatus == curStatus:
            self.nUnexpectedStatus += 1
        else:
            self.unexpectedStatus = curStatus
            self.nUnexpectedStatus = 0
        return False

    def run(self, *args, **kwargs) :
        pass