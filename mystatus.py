from typing import Dict, List, Optional
import logging
import time
import re
import tool
from icons import DMWorldIcon, GXWorldIcon, Icon, startGameIcon, notificationPageDownBar, generalReturnButton, kuloNoSuOccurPageLocator, kuloNoSuOccurPageGoTo, generalCloseButton,homePageMonsterGateNonSelected,homePageMonsterGateSelected, homePagePvpNonSelected,homePagePvpSelected,homePageStoreNonSelected,homePageStoreSelected,homePageTransportGateNonSelected,homePageTransportGateSelected,homePageWorkshopNonSelected,homePageWorkshopSelected,keysIcon, generalYesButton, normalNpcIcons, diagLogNextIcon, duelButton, autoDuelButton, saveVideoButton, recordButton, generalNextButton, duelResultsPageTitle, getSaiFragment, switchWorldButton, generalCancelButton 

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
                self.transferDict[action]()
                lastClickTime = time.time()
                logging.debug("lastClickTime {}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(lastClickTime))))
                time.sleep(delayTime)

class EmptyStatus(Status):
        pass

startPage = Status(
        name='startPage', 
        iconDict={"startGameIcon": startGameIcon},
        transferDict={
                "startGame": startGameIcon.click
        },
        condition='startGameIcon'
)

notificationPage = Status(
        name='notificationPage', 
        iconDict={
                "returnButton": generalReturnButton,
                "notificationPageDownBar": notificationPageDownBar
        },
        transferDict={"return": generalReturnButton.click},
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
                'selectPvp': homePagePvpNonSelected.click,
                'selectTransportGate': homePageTransportGateNonSelected.click,
                'selectStore': homePageStoreNonSelected.click,
                'selectMonsterGate': homePageMonsterGateNonSelected.click,
                'selectWorkshop': homePageWorkshopNonSelected.click,
                'collectOneKey': keysIcon.clickFirst,
                'collectAllKeys': keysIcon.clickAll,
                'clickOneNormalNpc': normalNpcIcons.clickFirst,
                'switchWorld': switchWorldButton.clickFirst
        },
        condition='pvpSelected | transportGateSelected | workshopSelected | storeSelected | monsterGateSelected'
)

recieveKeys = Status(
        name="recieveKeys",
        iconDict={
                'yesIcon': generalYesButton
        },
        transferDict={
                'click': generalYesButton.click
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
                'next': diagLogNextIcon.click
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
                'duel': duelButton.click,
                'autoDuel': autoDuelButton.click
        },
        condition='duelButton & autoDuelButton'
)

duelFinishedPage = Status(
        name="duelFinishedPage",
        iconDict={
                'saveVideoButton': saveVideoButton,
                'recordButton':  recordButton,
                'yes': generalYesButton,
        },
        transferDict={
                'saveVideo': saveVideoButton.click,
                'record': recordButton.click,
                'yes': generalYesButton.click
        },
        condition='saveVideoButton & recordButton & yes'
)

notFinishLoadingDuelResultsPage = Status(
        name="notFinishLoadingDuelResultsPage",
        iconDict={
                "next": generalNextButton,
                "title": duelResultsPageTitle
        },
        transferDict={
                'randomClick': duelResultsPageTitle.click
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
                'next': generalNextButton.click
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
                'yes': generalYesButton.click
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
                'switchToDMWorld': DMWorldIcon.click,
                'switchToGXWorld': GXWorldIcon.click
        },
        condition="dmWorld & gxWorld",
        level=200,
)

generalYesPage = Status(
        name='generalYesPage',
        iconDict={
                'yesButton': generalYesButton
        },
        transferDict={
                'yes': generalYesButton.click
        },
        condition="yesButton",
)

generalClosePage= Status(
        name='generalClosePage',
        iconDict={
                'closeButton': generalCloseButton
        },
        transferDict={
                'close': lambda status:generalCloseButton.click()
        },
        condition="closeButton",
)


generalNextPage= Status(
        name='generalNextPage',
        iconDict={
                'nextButton': generalNextButton
        },
        transferDict={
                'next': generalNextButton.click
        },
        condition="nextButton",
)

recommendFriendPage = Status(
        name='recommendFriendPage',
        iconDict={
                'cancelButton': generalCancelButton
        },
        transferDict={
                'cancel': generalCancelButton.click,
        },
        condition="cancelButton",
)
