from mystatus import Status, inDiagLog
from unionForce.icons import *
from general.icons import generalReturnButton, generalCloseButton
from unionForce.icons import unionForceChallengeButton

unionForcePage = Status(
    name = 'uionForcePage',
    iconDict={
        'title': unionForceTitle,
        'challengeButton': unionForceChallengeButton,
        'inDiagLog': inDiagLog,
        'returnButton': generalReturnButton,
        'closeButton': generalCloseButton
    },
    transferDict={
        'challenge': lambda status: unionForceChallengeButton.click(),
        'next': lambda status: inDiagLog.click(),
        'return': lambda status: generalReturnButton.click(),
        'close': lambda status: generalCloseButton.click()
    },
    condition='title'
)

