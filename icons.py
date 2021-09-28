import tool
import matplotlib.pyplot as plt
import os
import logging
import glob
from tool import HashableNdArray

class Icon:
        def __init__(self, path, name=None, similarity=0.8, check=True) -> None:
                self.path = path
                self.name = name
                self.similarity = similarity
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
                return tool.find_img(HashableNdArray(tool.get_appshot()), self.path, self.similarity)

        def exists(self) -> bool:
                return self.position is not None
        
        def showImg(self):
                plt.imshow(plt.imread(self.path))
                plt.show()

class SelectIcon(Icon):
        def __init__(self, selectPath, nonSelectPath) -> None:
                self.selectPath = selectPath       
                self.nonSelectPath = nonSelectPath

class MultiIcon(Icon):
        def __init__(self, paths, *args, **kwargs) -> None:
                if 'name' in kwargs:
                        self.name = kwargs['name']
                        del kwargs['name']
                self.icons = [Icon(path, *args, **kwargs) for path in paths]
                self.paths = paths

        def click(self, *args):
                self.clickFirst(*args)

        def clickAll(self, *args):
                for icon in self.icons:
                        if icon.exists():
                                icon.click(*args)

        def clickFirst(self, *args):
                for icon in self.icons:
                        if icon.exists():
                                icon.click(*args)
                                return
                raise Exception("MultiIcon {} can't be found!".format(self.paths))
        
        def count(self):
                n = 0
                for icon in self.icons:
                        if icon.exists():
                                n += 1
                return n

        def getFirstExistIcon(self):
                for icon in self.icons:
                        if icon.exists():
                                return icon
                raise Exception("No icon exist!")
        
        @property
        def position(self):
                return [icon.position for icon in self.icons]

        def exists(self) -> bool:
                return self.count() != 0

class CoordinateIcon(Icon):

        def __init__(self, position=None) -> None:
                self.path = None
                self._position = [
                        (position[0][0] * 2, position[0][1] * 2),
                        (position[1][0] * 2, position[1][1] * 2),
                ]
        
        @property
        def position(self):
            return self._position

        def click(self, x=0, y=0):
            return super().click(x=x, y=y)

        def exists(self) -> bool:
            return True

        def showImg(self):
                x, y = self._position
                img = tool.get_appshot()
                img = tool.get_appshot()[x[1]:y[1], x[0]:y[0]]
                plt.imshow(img[..., -1::-1])

startGameIcon = Icon('img/base/start_game.png')

notificationPageDownBar = Icon('img/notificationDownBar.png')

kuloNoSuOccurPageLocator = Icon('img/kuloNoSuOccurPage.png')
kuloNoSuOccurPageGoTo = Icon('img/kuloNoSuOccurGoTo.png')

diagLogNextIcon = Icon('img/diagLogNextIcon.png')
diagLogBackground = Icon('img/diagLogBackground.png')
diagLogTitleIcon = Icon('img/diagLogTitleIcon.png')

getSaiFragment = Icon('img/getSaiFragments.png')
