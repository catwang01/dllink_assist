from typing import Dict, Optional
from duel.icons import *
from general.icons import generalReturnButton, generalYesButton, generalNextButton
from mystatus import Status
from card import Card

class SelectDuelMode(Status):

    def leftZeroAutoDuel(self):
        return not self.iconDict['autoDuelButton'].exists()

selectDuelMode = SelectDuelMode(
        name="selectDuelMode",
        iconDict={
                'duelButton': duelButton,
                'autoDuelButton':  autoDuelButton,
                'autoDuelOffButton': autoDuelOffButton,
                'returnButton': generalReturnButton
        },
        transferDict={
                'manualduel': lambda status: duelButton.click(),
                'autoDuel': lambda status: autoDuelButton.click(),
                'return': lambda status: generalReturnButton.click()
        },
        condition='duelButton | autoDuelButton | autoDuelOffButton'
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

duelResultsPage = Status(
        name="duelResultsPage",
        iconDict={
                "next": generalNextButton,
                "title": duelResultsPageTitle,
                "yes": generalYesButton
        },
        transferDict={
                'next': lambda status: generalNextButton.click(),
                'randomClick': lambda status:duelResultsPageTitle.click(),
                'yes': lambda status: generalYesButton.click()
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
                'wait': lambda status: status
        },
        condition="autoControlButton",
)

class ManualDuelStatus(Status):

        def __init__(self, name: str, iconDict: Dict[str, Icon], transferDict, condition: str, subStatus: Optional[Dict[str, 'Status']] = None, level: str = 0, *args, **kwargs) -> None:
            super().__init__(name, iconDict, transferDict, condition, subStatus=subStatus, level=level, *args, **kwargs)
            if 'stages' not in kwargs:
                raise Exception(f'ManualDuelStatus requires stages!')
            self.stages = kwargs['stages']

        def getCurrentStage(self):
                for stage in self.stages:
                        if stage.exists():
                                return stage
                return None

        def hasEndTurnButton(self):
                return self.iconDict['endTurnButton'].exists()
        
        def hasBattleButton(self):
                return self.iconDict['battleButton'].exists()

        def hasActionButton(self):
                return self.iconDict['actionButton'].exists()

        def canUseSkill(self):
                return self.iconDict['skillButton'].exists()

        def isFirstTurn(self):
                return self.iconDict['firstTurnIcon'].exists()


useSkillPage = Status(
        name = 'useSkillPage',
        iconDict={
                'useSkillButton': useSkillButton,
                'useSkillPageTitle': useSkillPageTitle
        },
        transferDict={
                'useSkill': lambda status: useSkillButton.click()
        },
        condition='useSkillPageTitle',
        level=200
)

manualDuelStatus = ManualDuelStatus(
        name="manualDuelStatus",
        iconDict={
                "autoControlButton": autoControlButton,
                "autoControlOffButton": autoControlOffButton,
                "actionButton": actionButton,
                "battleButton": battleButton,
                'endTurnButton': endTurnButton,
                'blankPlace': blankPlace,
                'skillButton': skillButton,
                'firstTurnIcon': firstTurnIcon,
                'sumonButton': sumonButton,
                'setCardButton': setCardButton,
                'useCardButton': useCardButton,
                'perspectiveSwitchButton': perspectiveSwitchButton,
                'settingButton': settingButton
        },
        transferDict={
                'wait': lambda status: status,
                "showAction": lambda status: actionButton.click(),
                "battle": lambda status: battleButton.click(),
                "endTurn": lambda status: endTurnButton.click(),
                'clickUseSkillButton': lambda status: skillButton.click(),
                'sumon': lambda status: sumonButton.click(),
                'useCard': lambda status: useCardButton.click(),
                "clickBlank": lambda status: blankPlace.click(),
        },
        condition="settingButton",
        stages = [
                yourDrawCardPhraseIcon,
                yourMainPhraseIcon,
                yourBattlePhraseIcon,
                rivalPharseIcon
        ]
)

def selectTargetByCard(status, card):
        if isinstance(card, Card):
                card.init()
        card.click()

selectTargetPage = Status(
        name="selectTargetPage",
        iconDict={
                "title": selectTargetPageTitle,
                "confirmButton": selectTargetConfirmButton
        },
        transferDict={
                "selectTargetByCard": selectTargetByCard,
                "confirm": lambda status: selectTargetConfirmButton.click()
        },
        condition="title",
        level=200
)