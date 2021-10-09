from mystatus import Status
from homepage.icons import *
from general.icons import generalYesButton
from tool import Operation, get_appshot
from role import RoleCollection
from const import ROLE_DICT_FILE

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
        
        def getCurrentWorld(self, img=None):
                roleCollection = RoleCollection(ROLE_DICT_FILE)
                for name, role in roleCollection.roleDict.items():
                        if Icon(role.homePageImgPath, background=img).exists():
                                return role.world
                return 'DM'

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
                'switchWorldButton': switchWorldButton,
                'saiEnterButton': saiEnterButton,
                'unionForceIcon': unionForceIcon

        },
        transferDict={
                'selectPvp': lambda status:homePagePvpNonSelected.click(),
                'selectTransportGate': lambda status:homePageTransportGateNonSelected.click(),
                'enterTransportGate': lambda status:homePageTransportGateSelected.click(),
                'selectStore': lambda status:homePageStoreNonSelected.click(),
                'selectMonsterGate': lambda status:homePageMonsterGateNonSelected.click(),
                'selectWorkshop': lambda status:homePageWorkshopNonSelected.click(),
                'collectOneKey': lambda status:keysIcon.clickFirst(),
                'collectAllKeys': lambda status:keysIcon.clickAll(),
                'clickOneNormalNpc': lambda status:normalNpcIcons.clickFirst(),
                'switchWorld': lambda status:switchWorldButton.click(),
                'gotoSaiHomePage': lambda status: saiEnterButton.click(),
                'enterUionForce': lambda status: unionForceIcon.click(),
                'click': lambda status, point: Operation().click(point)
        },
        condition='pvpSelected | transportGateSelected | workshopSelected | storeSelected | monsterGateSelected'
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