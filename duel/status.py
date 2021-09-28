from duel.icons import *
from general.icons import generalReturnButton, generalYesButton, generalNextButton
from mystatus import Status

class SelectDuelMode(Status):

    def leftZeroAutoDuel(self):
        return False
        # self.iconDict['leftZeroButton'].exists()
        # self.iconDict['leftZeroButton'].showImg()

selectDuelMode = SelectDuelMode(
        name="selectDuelMode",
        iconDict={
                'duelButton': duelButton,
                'autoDuelButton':  autoDuelButton,
                'leftZeroButton': leftZeroAutoButton,
                'return': generalReturnButton
        },
        transferDict={
                'duel': lambda status: duelButton.click(),
                'autoDuel': lambda status :autoDuelButton.click(),
                'return': lambda status: generalReturnButton.click()
        },
        condition='duelButton & autoDuelButton'
)

class FinishedStatus(Status):

        def isWin(self):
                return self.iconDict['duelWinIcon'].exists()
        
duelFinishedPage = FinishedStatus(
        name="duelFinishedPage",
        iconDict={
                'saveVideoButton': saveVideoButton,
                'recordButton':  recordButton,
                'yes': generalYesButton,
                'duelWinIcon': duelWinIcon
        },
        transferDict={
                'saveVideo': lambda status:saveVideoButton.click(),
                'record': lambda status:recordButton.click(),
                'yes': lambda status:generalYesButton.click()
        },
        condition='recordButton & yes'
)

class DuelResultsPage(Status):

        def isLoaded(self):
                return self.iconDict['next'].exists()

duelResultsPage = DuelResultsPage(
        name="duelResultsPage",
        iconDict={
                "next": generalNextButton,
                "title": duelResultsPageTitle
        },
        transferDict={
                'next': lambda status: generalNextButton.click(),
                'randomClick': lambda status:duelResultsPageTitle.click()
        },
        condition="title",
        level=199,
)

inDuelStatus = Status(
        name="inDuelStatus",
        iconDict={
                "autoControlButton": autoControlButton
        },
        transferDict={
                'wait': lambda x: x
        },
        condition="autoControlButton",
)