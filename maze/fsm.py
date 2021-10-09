import logging
from FSM import FSM
from maze.status import *
from login.status import loginPage
from login.fsm import LoginFSM
from duel.status import selectDuelMode
from duel.fsm import DuelFSM
from general.status import generalStatusList
from mystatus import inDiagLog

class AddCardFSM(FSM):

    statusList = [addCardsStatus]
    def run(self, *args, **kwargs):
        self.initRun()
        while True:
            curStatus = self.getCurrentStatus()
            if curStatus == addCardsStatus:
                if curStatus.hasChecked():
                    curStatus.transfer('add')
                elif curStatus in generalStatusList:
                    curStatus.transfer('default')
                elif curStatus in loginPage:
                    LoginFSM().run()
                else:
                    curStatus.transfer("check")
            else:
                if self.handleUnexpectedStatus(curStatus):
                    break
        return

class MazeFSM(FSM):

    statusList=floorStatusList + [
            guessCoinPage,
            selectDuelMode,
            addCardsStatus
    ] + generalStatusList

    name = 'MazeFSM'

    def run(self):
        self.beforeRun()
        while True:
            curStatus = self.getCurrentStatus()
            if curStatus in floorStatusList:
                curStatus.transfer('next')
            elif curStatus == guessCoinPage:
                curStatus.transfer('select2')
            elif curStatus == addCardsStatus:
                AddCardFSM().run()
            elif curStatus == inDiagLog:
                curStatus.transfer('next')
            elif curStatus == selectDuelMode:
                DuelFSM().run()
            elif curStatus in generalStatusList:
                curStatus.transfer("default")
            else:
                if self.handleUnexpectedStatus(curStatus):
                    break
        self.afterRun()
        return