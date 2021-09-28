from icons import Icon
from typing import Dict, Optional, List
from mystatus import Status
from maze.icons import *

class StepStatus(Status):

    def __init__(self, 
        name: str, 
        iconDict: Dict[str, Icon], 
        transferDict, 
        condition: str, 
        subStatus: Optional[Dict[str, 'Status']] = None, 
        level: str = 0, 
        nextDirection=None,
        *args, **kwargs) -> None:
        super().__init__(name, iconDict, transferDict, condition, subStatus=subStatus, level=level, *args, **kwargs)
        if nextDirection is None:
            raise Exception("StepStatus requires 'nextDirection' arg!") 
        self.nextDirection = nextDirection
        self.imgBeforeClick = None

    def getImgBeforeClick(self):
        self.imgBeforeClick = self.iconDict['currentLocation'].getClickImg(self.nextDirection)

    def isSuccess(self):
        imgAfterBeforeClick = self.iconDict['currentLocation'].getClickImg(self.nextDirection)
        return imgAfterBeforeClick != self.imgBeforeClick

def nextStep(status):
    status.getImgBeforeClick() 
    currentLocation.clickWithDirection(status.nextDirection)

floorStatusList = []
globalLevel = 100

def registerFloorStatus(nextDirection, icon, floorStatusList):
    global globalLevel
    floorStatus = StepStatus(
        name=icon.name,
        iconDict={
            'mazeTitle':  mazeTitleIcon,
            'currentLocation': currentLocation,
            name: icon
        },
        transferDict={
            'next': nextStep
        },
        condition="mazeTitle & {}".format(name),
        level=globalLevel,
        nextDirection=nextDirection
    )
    floorStatusList.append(floorStatus)
    globalLevel += 1
    return floorStatus

for icon in stepIcons:
    registerFloorStatus(icon.nextDirection, icon, floorStatusList)

guessCoinPage = Status(
    name='guessCoinPage',
    iconDict={
        'guessCoinIcon': guessCoinIcon,
        'select2Icon': guessCoinSelect2
    },
    transferDict={
        'select2': lambda status:  guessCoinIcon.click(),
        'default': lambda status:  guessCoinIcon.click()
    },
    condition="guessCoinIcon",
)

inMazeStatus = Status(
    name='inMazeStatus',
    iconDict={
        'mazeTitle':  mazeTitleIcon,
        'currentLocation': currentLocation 
    },
    transferDict={
    },
    condition="mazeTitle",
)

class AddCardsStatus(Status):

    def hasChecked(self):
        return self.iconDict['checkedIcon'].exists()

addCardsStatus = AddCardsStatus(
    name='addCardsStatus',
    iconDict={
        'addToStorageIcon':  addToStorageIcon,
        'checkedIcon': checkedIcon,
        'checkBlank': checkBlank, 
        'selectCardsLocator': selectCardsLocator
    },
    transferDict={
        'check': lambda status: checkBlank.click(),
        'add': lambda status: addToStorageIcon.click()
    },
    condition="selectCardsLocator",
)