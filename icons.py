import tool
import os
import logging
import glob
from tool import HashableNdArray

class Icon:
        def __init__(self, path, check=True) -> None:
                self.path = path
                if check and not os.path.exists(self.path):
                        raise Exception("Can't find img: {}".format(self.path))



        def click(self, x=0, y=0):
                if not self.exists():
                        raise Exception("Icon {} can't be clicked, because it doesn't exist!".format(self.path))
                centerPoint = tool.get_center_point(self.position)
                centerPoint = [x + centerPoint[0] / 2, y + centerPoint[1] / 2]
                tool.Operation().click(centerPoint)
                logging.debug("Click {} finished".format(self.path))

        @property
        def position(self):
                return tool.find_img(HashableNdArray(tool.get_appshot()), self.path)

        def exists(self) -> bool:
                return self.position is not None

class SelectIcon(Icon):
        def __init__(self, selectPath, nonSelectPath) -> None:
                self.selectPath = selectPath       
                self.nonSelectPath = nonSelectPath

class MultiIcon(Icon):
        def __init__(self, paths) -> None:
                self.icons = [Icon(path) for path in paths]
                self.paths = paths

        def clickAll(self):
                for icon in self.icons:
                        if icon.exists():
                                icon.click()

        def clickFirst(self):
                for icon in self.icons:
                        if icon.exists():
                                icon.click()
                                return
                raise Exception("MultiIcon {} can't be found!".format(self.paths))
        
        def count(self):
                n = 0
                for icon in self.icons:
                        if icon.exists():
                                n += 1
                return n
        
        @property
        def position(self):
                return [icon.position for icon in self.icons]

        def exists(self) -> bool:
                return self.count() != 0

keysIcon = MultiIcon(glob.glob('img/base/key*.png'))

startGameIcon = Icon('img/base/start_game.png')

notificationPageDownBar = Icon('img/notificationDownBar.png')

kuloNoSuOccurPageLocator = Icon('img/kuloNoSuOccurPage.png')
kuloNoSuOccurPageGoTo = Icon('img/kuloNoSuOccurGoTo.png')

generalYesButton = Icon('img/base/generalYesButton.png')
generalReturnButton = Icon('img/returnButton.png')
generalCloseButton = Icon('img/closeButton.png')
generalNextButton = Icon('img/generalNextButton.png')
generalCancelButton = Icon('img/generalCancelButton.png')

homePageTransportGateSelected = Icon('img/home/channels/transport_gate_selected.png')
homePageTransportGateNonSelected = Icon('img/home/channels/transport_gate_non_selected.png')

homePagePvpSelected = Icon('img/home/channels/pvp_selected.png')
homePagePvpNonSelected = Icon('img/home/channels/pvp_non_selected.png')

homePageStoreSelected = Icon('img/home/channels/store_selected.png')
homePageStoreNonSelected = Icon('img/home/channels/store_non_selected.png')

homePageMonsterGateSelected = Icon('img/home/channels/monster_gate_selected.png')
homePageMonsterGateNonSelected = Icon('img/home/channels/monster_gate_non_selected.png')

homePageWorkshopSelected = Icon('img/home/channels/workshop_selected.png')
homePageWorkshopNonSelected = Icon('img/home/channels/workshop_non_selected.png')

normalNpcIcons = MultiIcon(glob.glob('img/npc/npc*.png'))

diagLogNextIcon = Icon('img/diagLogNextIcon.png')

duelButton = Icon('img/duelButton.png')
autoDuelButton = Icon('img/autoDuelButton.png')


saveVideoButton = Icon('img/saveVideo.png')
recordButton = Icon('img/recordButton.png')

duelResultsPageTitle = Icon('img/duelResultsPageTitle.png')
duelWinIcon  = Icon('img/duelWinIcon.png')

getSaiFragment = Icon('img/getSaiFragments.png')

switchWorldButton = MultiIcon(glob.glob('img/switchWorldButton*.png'))

DMWorldIcon = Icon('img/DMWorldIcon.png')
GXWorldIcon = Icon('img/GXWorldIcon.png')
