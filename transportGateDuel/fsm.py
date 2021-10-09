from FSM import FSM
from transportGateDuel.status import *
from mystatus import inDiagLog
from homepage.status import homePage
from duel.status import selectDuelMode
from duel.fsm import AutoDuelFSM, DuelFSM, ManualDuelFSM
from general.status import generalStatusList

class TransportGateFSM(FSM):

    statusList = [
        transportGateHomePage,
        inDiagLog,
        selectDuelMode,
        homePage,
        npcAlreadyExistsStatus
    ] + generalStatusList

    name = 'TransportGateFSM'

    def __init__(self) -> None:
        super().__init__()
        self.autoDuelable = True

    def getWorldFromRole(self, roleName):
        return {'yukijudai': 'gx', 'tianjoyin': 'gx', 'mutouyougi': 'dm'}.get(roleName, None)

    def run(self, roleName: str, level: str, duelFSM):
        self.beforeRun()
        world = self.getWorldFromRole(roleName)
        clicked = False
        while True:
            nowStatus = self.getCurrentStatus()
            if nowStatus == transportGateHomePage:
                if isinstance(duelFSM, AutoDuelFSM) and not self.autoDuelable:
                    nowStatus.transfer('return')
                elif not nowStatus.isCurrentRole:
                    if not nowStatus.isSwitchingRole():
                        nowStatus.transfer('selectRoles')
                    elif nowStatus.hasRole(roleName):
                        if not clicked:
                            nowStatus.transfer(roleName)
                            clicked = True
                        elif nowStatus.hasYes():
                            nowStatus.transfer('yes')
                            nowStatus.isCurrentRole = True
                        elif nowStatus.hasClose():
                            nowStatus.transfer('close')
                            nowStatus.isCurrentRole = True
                    else:
                        if not nowStatus.isPopup():
                            nowStatus.transfer('selectWorld')
                        else:
                            nowStatus.transfer('select{}'.format(world.upper()))
                else:
                    if nowStatus.canGetLevel():
                        if nowStatus.getLevel() != level:
                            nowStatus.transfer(level)
                        else:
                            nowStatus.transfer('duel')
            elif nowStatus == npcAlreadyExistsStatus:
                nowStatus.transfer('confirm')
            elif nowStatus == inDiagLog:
                nowStatus.transfer('next')
            elif nowStatus == selectDuelMode:
                self.autoDuelable = DuelFSM().run(duelFSM)
            elif nowStatus in generalStatusList:
                nowStatus.transfer("default")
            elif nowStatus == homePage:
                break
            else:
                if self.handleUnexpectedStatus(nowStatus):
                    break
        self.afterRun()
        return