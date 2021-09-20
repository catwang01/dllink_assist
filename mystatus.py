from typing import Dict, List, Optional
import logging
import time
import re
import tool
from icons import *
from general.icons import *

lastClickTime = -1

class Status:
        def __init__(self, 
                        name: str, 
                        iconDict: Dict[str, Icon], 
                        transferDict,
                        condition: str,
                        subStatus: Optional[Dict[str, 'Status']] = None,
                        level: str=0,
                        *args,
                        **kwargs) -> None:
                self.name = name
                self.iconDict = iconDict
                self.transferDict = transferDict
                self.condition = self.conditionParse(condition)
                self.subStatus = [] if subStatus is None else subStatus
                self.subStatus.sort(key=lambda x: x.level, reverse=True)
                self.level = level

        def check(self) -> bool:
                return eval(self.condition)
                
        def __str__(self):
                return self.name

        def conditionParse(self, conditionStr: str):
                words = re.findall('[a-z0-9A-Z]+', conditionStr)
                for word in words:
                        if word in self.iconDict:
                                conditionStr = conditionStr.replace(word, 'self.iconDict["{}"].exists()'.format(word))
                conditionStr = conditionStr.replace('|', ' or ')
                conditionStr = conditionStr.replace('&', ' and ')
                conditionStr = conditionStr.replace('!', ' not ')
                return conditionStr

        def transfer(self, action: str, delayTime: int = 0) -> None:
                global lastClickTime
                if action not in self.transferDict:
                        raise Exception("act {} not in {}".format(action, self.transferDict))
                logging.debug("CurrentStatus: {}. Take action {}".format(self.name, action))
                func = self.transferDict[action]
                func(self)
                lastClickTime = time.time()
                logging.debug("lastClickTime {}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(lastClickTime))))
                time.sleep(delayTime)

class EmptyStatus(Status):
        pass

startPage = Status(
        name='startPage', 
        iconDict={"startGameIcon": startGameIcon},
        transferDict={
                "startGame": lambda status: startGameIcon.click()
        },
        condition='startGameIcon'
)

notificationPage = Status(
        name='notificationPage', 
        iconDict={
                "returnButton": generalReturnButton,
                "notificationPageDownBar": notificationPageDownBar
        },
        transferDict={
                "return": lambda status: generalReturnButton.click()
        },
        condition='notificationPageDownBar'
)

kuloNoSuOccurPage = Status(
        name='kuloNoSuOccurPage',
        iconDict={
                "closeButton": generalCloseButton, 
                "gotoButton": kuloNoSuOccurPageGoTo,
                "locator": kuloNoSuOccurPageLocator
        },
        transferDict={
                "close": generalCloseButton.click,
                "goto": kuloNoSuOccurPageGoTo.click
        },
        condition='locator'
)


class HomePage(Status):

        def hasKeys(self):
                return self.iconDict['keys'].exists()
        
        def countKeys(self):
                return self.iconDict['keys'].count()

        def inWhichChannel(self) -> str:
                for name, icon in self.iconDict.items():
                        if name.endswith("Selected") and not name.endswith("NonSelected") and icon.exists():
                                return name[:-len('Selected')]
                raise Exception("Channel not found")
        
        def hasNormalNpcs(self):
                return self.iconDict['normalNpcs'].exists()

        def countNormalNpcs(self):
                return self.iconDict['normalNpcs'].count()
        
        def getCurrentWorld(self):
                pass

homePage = HomePage(
        name='homePage',
        iconDict={
                'pvpSelected': homePagePvpSelected,
                'pvpNonSelected': homePagePvpNonSelected,
                'transportGateNonSelected': homePageTransportGateNonSelected,
                'transportGateSelected': homePageTransportGateSelected,
                'storeNonSelected': homePageStoreNonSelected,
                'storeSelected': homePageStoreSelected,
                'monsterGateNonSelected': homePageMonsterGateNonSelected,
                'monsterGateSelected': homePageMonsterGateSelected,
                'workshopSelected': homePageWorkshopSelected,
                'workshopNonSelected': homePageWorkshopNonSelected,
                'keys': keysIcon,
                'normalNpcs': normalNpcIcons,
                'switchWorldButton': switchWorldButton
        },
        transferDict={
                'selectPvp': lambda status:homePagePvpNonSelected.click(),
                'selectTransportGate': lambda status:homePageTransportGateNonSelected.click(),
                'selectStore': lambda status:homePageStoreNonSelected.click(),
                'selectMonsterGate': lambda status:homePageMonsterGateNonSelected.click(),
                'selectWorkshop': lambda status:homePageWorkshopNonSelected.click(),
                'collectOneKey': lambda status:keysIcon.clickFirst(),
                'collectAllKeys': lambda status:keysIcon.clickAll(),
                'clickOneNormalNpc': lambda status:normalNpcIcons.clickFirst(),
                'switchWorld': lambda status:switchWorldButton.click()
        },
        condition='pvpSelected | transportGateSelected | workshopSelected | storeSelected | monsterGateSelected'
)

recieveKeys = Status(
        name="recieveKeys",
        iconDict={
                'yesIcon': generalYesButton
        },
        transferDict={
                'click': lambda status:generalYesButton.click()
        },
        condition='homePage.check() & yesIcon',
        level = 200
)

inDiagLog = Status(
        name="inDiagLog",
        iconDict={
                'nextButton': diagLogNextIcon
        },
        transferDict={
                'next': lambda status:diagLogNextIcon.click()
        },
        condition='nextButton'
)

selectDuelMode = Status(
        name="selectDuelMode",
        iconDict={
                'duelButton': duelButton,
                'autoDuelButton':  autoDuelButton
        },
        transferDict={
                'duel': lambda status: duelButton.click(),
                'autoDuel': lambda status :autoDuelButton.click()
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

notFinishLoadingDuelResultsPage = Status(
        name="notFinishLoadingDuelResultsPage",
        iconDict={
                "next": generalNextButton,
                "title": duelResultsPageTitle
        },
        transferDict={
                'randomClick': lambda status:duelResultsPageTitle.click()
        },
        condition="title & !next",
        level=200
)

duelResultsPage = Status(
        name="duelResultsPage",
        iconDict={
                "next": generalNextButton,
                "title": duelResultsPageTitle
        },
        transferDict={
                'next': lambda status:generalNextButton.click()
        },
        condition="title & next",
        level=199,
)

getSaiStatus = Status(
        name="getSaiFragment",
        iconDict={
                "getSaiFragment": getSaiFragment,
                "yes": generalYesButton
        },
        transferDict={
                'yes': lambda status:generalYesButton.click()
        },
        condition="getSaiFragment",
        level=200,
)

switchingWorldStatus = Status(
        name="switchingWorldStatus",
        iconDict={
                'dmWorld': DMWorldIcon,
                'gxWorld': GXWorldIcon
        },
        transferDict={
                'switchToDMWorld': lambda status:DMWorldIcon.click(),
                'switchToGXWorld': lambda status:GXWorldIcon.click()
        },
        condition="dmWorld & gxWorld",
        level=200,
)
