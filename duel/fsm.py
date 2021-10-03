from FSM import FSM
import logging
from duel.status import *
from mystatus import getSaiStatus, inDiagLog
from general.status import generalStatusList
from login.status import loginPage
from login.fsm import LoginFSM
from homepage.status import homePage
from transportGateDuel.status import transportGateHomePage


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
        homePage
    ] + generalStatusList

    name = 'DuelFSM'

    def __init__(self) -> None:
        super().__init__()
        self.autoDualable = True

    def run(self):
        self.beforeRun()
        self.isWin = None
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
                self.isWin = curStatus.isWin()
                curStatus.transfer("yes")
            elif curStatus == duelResultsPage:
                if curStatus.isLoaded():
                    curStatus.transfer("next")
                else:
                    curStatus.transfer("randomClick")
            elif curStatus == getSaiStatus:
                curStatus.transfer("yes")
            elif curStatus in generalStatusList:
                curStatus.transfer("default")
            elif curStatus == loginPage:
                LoginFSM().run()
            elif curStatus == inDiagLog:
                curStatus.transfer('next')
            elif curStatus in {transportGateHomePage, homePage}:
                break
            else:
                if self.handleUnexpectedStatus(curStatus):
                    break
        self.afterRun()
        return self.autoDualable