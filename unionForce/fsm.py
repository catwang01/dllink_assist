from FSM import FSM
from unionForce.status import unionForcePage
from mystatus import inDiagLog
from duel.fsm import DuelFSM
from homepage.status import homePage
from duel.status import selectDuelMode

class UnionForceFSM(FSM):

    name = 'UnionForceFSM'
    statusList = [ 
        homePage,
        unionForcePage, 
        inDiagLog,
        selectDuelMode
    ]

    def run(self):
        self.beforeRun()
        nDuels = 0
        while True:
            curStatus = self.getCurrentStatus()
            if curStatus == unionForcePage:
                if curStatus.hasButton('challengeButton'):
                    curStatus.transfer('challenge')
                else:
                    curStatus.transfer('return')
            elif curStatus == inDiagLog:
                curStatus.transfer('next')
            elif curStatus == selectDuelMode:
                DuelFSM().run()
                nDuels += 1
                break
            elif curStatus == homePage:
                break
            else:
                if self.handleUnexpectedStatus(curStatus):
                    break
        self.afterRun()
        return nDuels