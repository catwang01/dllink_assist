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

        def hasButton(self, buttonName):
                if buttonName not in self.iconDict:
                        raise Exception(f'Status: {self.name} has no button {buttonName}')
                return self.iconDict[buttonName].exists()

        def transfer(self, action: str, delayTime: int = 0, args=(), kwargs={}) -> None:
                global lastClickTime
                if action not in self.transferDict:
                        raise Exception("act {} not in {}".format(action, self.transferDict))
                logging.debug("CurrentStatus: {}. Take action {}".format(self.name, action))
                func = self.transferDict[action]
                func(self, *args, **kwargs)
                lastClickTime = time.time()
                logging.debug(f"lastClickTime {tool.formatTime(lastClickTime)}")
                if delayTime > 0: 
                        tool.sleep(delayTime)

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
                "close": lambda status: generalCloseButton.click(),
                "goto": lambda status: kuloNoSuOccurPageGoTo.click()
        },
        condition='locator'
)


inDiagLog = Status(
        name="inDiagLog",
        iconDict={
                'nextButton': diagLogNextIcon,
                'title': diagLogTitleIcon,
                'background': diagLogBackground
        },
        transferDict={
                # 'next': lambda status: diagLogNextIcon.click()
                'next': lambda status: diagLogBackground.click()
        },
        condition='nextButton | background'
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
