from mystatus import Status
import re
from typing import Optional, Dict
from transportGateDuel.icons import *
from general.status import generalConfirmButton, generalCloseButton, generalYesButton, generalCancelButton
import logging
from log.log import setupLogging

setupLogging()
logger = logging.getLogger(__name__)

class TransportGateHomePage(Status):

    def __init__(self, name: str, iconDict: Dict[str, Icon], transferDict, condition: str, subStatus: Optional[Dict[str, 'Status']] = None, level: str = 0, *args, **kwargs) -> None:
        super().__init__(name, iconDict, transferDict, condition, subStatus=subStatus, level=level, *args, **kwargs)
        self.isCurrentRole = False

    def isSwitchingRole(self):
        return not self.iconDict['selectRoleIcon'].exists()

    def hasRole(self, roleName: str):
        return self.iconDict[roleName+ "Icon"].exists()

    def isPopup(self):
        return self.iconDict['dmTransportGateItem'].exists()

    def hasYes(self):
        return self.iconDict['yesIcon'].exists()

    def hasClose(self):
        return self.iconDict['closeIcon'].exists()

    def getLevel(self):
        iconPath = levelSelected.getFirstExistIcon().path
        reg = re.search("level\d+", iconPath)
        if reg is None:
            raise Exception("Can't exact level from path: {}".format(iconPath))
        return reg.group(0)

transportGateHomePage = TransportGateHomePage(
        name="transportGateHomePage",
        iconDict={
                'title': transportGatePageTitle,
                'bar': selectTransportGateBar,
                'gxTransportGateItem': gxTransportGateItem,
                'dmTransportGateItem': dmTransportGateItem,
                'selectRoleIcon': selectTransportGateRoles,

                'yukijudaiIcon': yukijudaiIcon,
                'tianjoyinIcon': tianjoyinIcon,
                'mutouyougiIcon': mutouyougiIcon,

                'yesIcon': generalConfirmButton,
                'closeIcon': generalCloseButton,

                'level10Icon': level10Button,
                'level20Icon': level20Button,
                'level30Icon': level30Button,
                'level40Icon': level40Button,
                'levelSelected': levelSelected,
                'duelIcon': transportGateDuelButton,
        },
        transferDict={
                'selectRoles': lambda status: selectTransportGateRoles.click(),
                'selectWorld': lambda status: selectTransportGateBar.click(),
                'selectDM': lambda status: dmTransportGateItem.click(),
                'selectGX': lambda status: gxTransportGateItem.click(),
                'yukijudai': lambda status: yukijudaiIcon.click(),
                'tianjoyin': lambda status: tianjoyinIcon.click(),
                'mutouyougi': lambda status: mutouyougiIcon.click(),
                'yes': lambda status: generalConfirmButton.click(),
                'close': lambda status: generalCloseButton.click(),
                'level10': lambda status: level10Button.click(),
                'duel': lambda status: transportGateDuelButton.click()
        },
        condition="title",
        level=200,
)


npcAlreadyExistsStatus = Status(
        name="transportGateHomePage",
        iconDict={
                'title': npcAlreadyExistsTitle,
                'confirmButton':  generalConfirmButton,
                'cancelButton': generalCancelButton
        },
        transferDict={
            'confirm': lambda status: generalConfirmButton.click()
        },
        condition="title",
        level=transportGateHomePage.level+1
)