from FSM import FSM
from general.status import generalStatusList
from activity.sai.status import *
from mystatus import inDiagLog
from duel.status import selectDuelMode
from duel.fsm import DuelFSM
from homepage.status import homePage

class SaiFSM(FSM):

    statusList = [
        homePage,
        saiHomePage, 
        inDiagLog,
        selectDuelMode,
        selectLevelPage,
        coinRepoPage,
        lotteryHomePage,
        useItemHomePage
    ] + generalStatusList
    statusList.sort(key=lambda icon: icon.level, reverse=True)

    name = 'SaiFSM'

    def run(self):
        self.beforeRun()
        isCoinEnough = True
        hasUsableItems = True
        while True:
            curStatus = self.getCurrentStatus()
            if curStatus == saiHomePage:
                if curStatus.canActivityDuel():
                    curStatus.transfer('activityDuel')
                elif curStatus.canFlipSai():
                    curStatus.transfer('flip')
                elif isCoinEnough and curStatus.canEnterLottery():
                    curStatus.transfer('enterLottery', 3)
                elif hasUsableItems:
                    curStatus.transfer('enterItemMenu', 3)
                else:
                    curStatus.transfer('return')
            elif isCoinEnough and curStatus == lotteryHomePage:
                if curStatus.canBuyLottery():
                    # wait close button appear
                    curStatus.transfer('buyLottery', 3)
                elif curStatus.hasClose():
                    curStatus.transfer('close')
                else:
                    curStatus.transfer('return')
                    isCoinEnough = False
            elif hasUsableItems and curStatus == useItemHomePage:
                if curStatus.hasUsableItem():
                    curStatus.transfer('useItem')
                else:
                    if curStatus.hasClose():
                        curStatus.transfer('close')
                    hasUsableItems = False
            elif curStatus == selectLevelPage:
                curStatus.transfer('selectDifficultLevel')
            elif curStatus == coinRepoPage:
                curStatus.transfer("yes")
            elif curStatus == inDiagLog:
                curStatus.transfer('next')
            elif curStatus == selectDuelMode:
                DuelFSM().run()
            elif curStatus in generalStatusList:
                curStatus.transfer('default', 2)
            elif curStatus == homePage:
                break
            else:
                if self.handleUnexpectedStatus(curStatus):
                    break
        self.afterRun()
        return

