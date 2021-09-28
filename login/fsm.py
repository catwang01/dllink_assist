from login.status import *
from FSM import FSM

class LoginFSM(FSM):

    statusList = [
        loginPage
    ]

    name = 'LoginFSM'

    def run(self):
        self.beforeRun()
        while True:
            curStatus = self.getCurrentStatus()
            if curStatus == loginPage:
                if curStatus.hasLoginButton():
                    curStatus.transfer('login')
                elif curStatus.hasAuthorizeButton():
                    curStatus.transfer('authorize')
                elif curStatus.hasIKnowButton():
                    curStatus.transfer("iKnow")
            else:
                if self.handleUnexpectedStatus(curStatus):
                    break
        self.afterRun()
        return