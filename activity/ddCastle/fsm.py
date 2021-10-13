from FSM import FSM
from general.status import generalStatusList
from activity.ddCastle.status import *
from duel.status import inDuelStatus, duelResultsPage
from duel.fsm import DuelFSM

class DDCastleFSM(FSM):

    name = "DDCastleFSM"
    statusList = [ddCastleHomePage, ddCastleLotteryHomePage, inDuelStatus] + generalStatusList

    def run(self):
        self.beforeRun()
        while True:
            curStatus = self.getCurrentStatus()
            if curStatus == ddCastleHomePage:
                if not curStatus.hasButton('firstFloorIcon'):
                    curStatus.transfer('downSlide')
                elif curStatus.hasButton('autoDuelButton'):
                    curStatus.transfer('autoDuel')
                else:
                    if curStatus.hasButton('cardLotteryButton'):
                        curStatus.transfer('enterLottery')
                    else:
                        curStatus.transfer('return')
            elif curStatus == ddCastleLotteryHomePage:
                if curStatus.hasButton('buyLotteryButton'):
                    curStatus.transfer("buyLottery")
                elif curStatus.hasButton('closeButton'):
                    curStatus.transfer('close')
                else:
                    curStatus.transfer('return')
            elif curStatus == inDuelStatus:
                DuelFSM().run()
            elif curStatus in generalStatusList:
                curStatus.transfer('default')
            else:
                if self.handleUnexpectedStatus(curStatus):
                    break
        self.afterRun()
        return