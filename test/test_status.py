import sys
import os
thisFile = __file__
sys.path.append(os.path.dirname(os.path.dirname(thisFile)))
from mystatus import Status
from homepage.status import homePageMonsterGateNonSelected, homePageMonsterGateSelected, homePagePvpNonSelected, homePagePvpSelected, homePageStoreNonSelected, homePageStoreSelected, homePageTransportGateNonSelected, homePageTransportGateSelected, homePageWorkshopSelected, homePageWorkshopNonSelected


class TestStatus:

        def testConditionParse(self):
                icon = Status(
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
                        },
                        transferDict={
                                'selectPvp': homePagePvpNonSelected.click,
                                'selectTransportGate': homePageTransportGateNonSelected.click,
                                'selectStore': homePageStoreNonSelected.click,
                                'selectMonsterGate': homePageMonsterGateNonSelected.click,
                                'selectWorkshop': homePageWorkshopNonSelected.click,
                        },
                        condition='pvpSelected | transportGateSelected | workshopSelected | storeSelected | monsterGateSelected'
                )
                assert icon.conditionParse('pvpSelected|transportGateSelected') == 'self.iconDict["pvpSelected"].exists() or self.iconDict["transportGateSelected"].exists()'
                assert icon.conditionParse('pvpSelected&transportGateSelected') == 'self.iconDict["pvpSelected"].exists() and self.iconDict["transportGateSelected"].exists()'
                assert icon.conditionParse('pvpSelected&!transportGateSelected') == 'self.iconDict["pvpSelected"].exists() and  not self.iconDict["transportGateSelected"].exists()'