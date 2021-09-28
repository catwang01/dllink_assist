from mystatus import Status
from login.icons import *

class LoginPage(Status):

    def hasLoginButton(self):
        return self.iconDict['loginButton'].exists()

    def hasAuthorizeButton(self):
        return self.iconDict['authorizeButton'].exists()

    def hasIKnowButton(self):
        return self.iconDict['iKnowButton'].exists()

loginPage = LoginPage(
        name="loginPage",
        iconDict={
            'loginButton': loginButton, 
            'authorizeButton': authorizeButton,
            'iKnowButton': iKnowButton
        },
        transferDict={
            'login': lambda status: loginButton.click(),
            'authorize': lambda status: authorizeButton.click(),
            'iKnow': lambda status: iKnowButton.click()
        },
        condition="authorizeButton | iKnowButton | loginButton",
        level=300,
)
