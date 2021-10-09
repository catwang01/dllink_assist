from mystatus import Status, inDiagLog
from unionForce.icons import *
from general.icons import generalReturnButton

unionForcePage = Status(
    name = 'uionForcePage',
    iconDict={
        'title': unionForceTitle,
        'challengeButton': unionForceChallengeButton,
        'inDiagLog': inDiagLog,
        'returnButton': generalReturnButton
    },
    transferDict={
        'challenge': lambda status: unionForceChallengeButton.click(),
        'next': lambda status: inDiagLog.click(),
        'return': lambda status: generalReturnButton.click()
    },
    condition='title'
)

