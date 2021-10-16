import tool
import matplotlib.pyplot as plt
import os
import logging
import glob
import cv2
from tool import HashableNdArray
from inference import DetectObject
from const import ICON_DEFAULT_SLEEP_CLICK_TIME

class Icon:
        def __init__(self, path, name=None, check=True, background=None, clickSleepTime=None, *args, **kwargs) -> None:
                self.path = path
                self.name = name
                if clickSleepTime is None:
                        self.clickSleepTime = ICON_DEFAULT_SLEEP_CLICK_TIME
                else:
                        self.clickSleepTime = clickSleepTime
                if check and not os.path.exists(self.path):
                        raise Exception("Can't find img: {}".format(self.path))
                self.img = cv2.imread(self.path)

                self._background = None
                self.background = background

                # used for tool.find_img
                self.args = args
                self.kwargs = kwargs

        def __repr__(self) -> str:
            return f"Icon(name='{self.name}', path='{self.path}', clickSleepTime={self.clickSleepTime})"

        def click(self, x=0, y=0):
                if not self.exists():
                        raise Exception(f"Icon {self} can't be clicked, because it doesn't exist!")
                centerPoint = tool.get_center_point(self.position)
                centerPoint = [x + centerPoint[0] / 2, y + centerPoint[1] / 2]
                tool.Operation().click(centerPoint)
                logging.debug(f"Click {self} finished")
                if self.clickSleepTime > 0:
                        tool.sleep(self.clickSleepTime)

        @property
        def background(self):
                if self._background is None:
                        # logging.debug(f"background of Icon is not set. Use appshot.")
                        return tool.get_appshot()
                else:
                        return self._background

        @background.setter
        def background(self, background):
                if background is not None:
                        if isinstance(background, str):
                                background = cv2.imread(background)
                        self._background = background.copy()

        @property
        def position(self):
                return tool.find_img(self.background, self.img, *self.args, **self.kwargs)

        def exists(self) -> bool:
                return self.position is not None
        
        def showImg(self, showBackground=True):
                if showBackground:
                        plt.subplot(121)
                        tool.imshow(self.img)
                        plt.subplot(122)
                        tool.imshow(self.background)
                else:
                        tool.imshow(self.img)
                plt.show()

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

        @property
        def background(self):
                if self._background is None:
                        # logging.debug(f"background of Icon is not set. Use appshot.")
                        return tool.get_appshot()
                else:
                        return self._background

        @background.setter
        def background(self, background):
                if background is not None:
                        if isinstance(background, str):
                                background = cv2.imread(background)
                        self._background = background.copy()


class CoordinateIcon(Icon):

        def __init__(self, position=None, name=None, background=None, clickSleepTime=0.5) -> None:
                self.path = None
                self.name = name
                self._background = None
                self.background = background

                self._position = [
                        (position[0][0] * 2, position[0][1] * 2),
                        (position[1][0] * 2, position[1][1] * 2),
                ]
                self.clickSleepTime = clickSleepTime
        
        @property
        def position(self):
            return self._position

        def click(self, x=0, y=0):
                centerPoint = tool.get_center_point(self.position)
                centerPoint = [x + centerPoint[0] / 2, y + centerPoint[1] / 2]
                tool.Operation().click(centerPoint)
                logging.debug(f"Click {self} finished")
                if self.clickSleepTime > 0:
                        tool.sleep(self.clickSleepTime)
                return centerPoint

        def __repr__(self) -> str:
            return f"CoordinateIcon(name={self.name}, position={self.position})"

        def exists(self) -> bool:
            return True

        def getImg(self):
                x, y = self._position
                return self.background[x[1]:y[1], x[0]:y[0]]

        def showImg(self):
                tool.imshow(self.getImg())

class Yolov5Icon(MultiIcon):
        def __init__(self, path, name=None, class_=None, classes=None, check=True) -> None:
                self.path = path
                self.name = name
                if class_ is None:
                        raise Exception("Yolov5Icon: class_ can be None")
                self.class_ = class_
                self.classes = classes
                self.class2Index = {name: i for i, name in enumerate(classes)}
                if check and not os.path.exists(self.path):
                        raise Exception("Can't find model weights: {}".format(self.path))
                self.model = DetectObject(weights=self.path, classes=self.classes)
                self._icons = None

        @property
        def icons(self):
                self._icons = []
                img, predResults = self.model.detect(tool.get_appshot())
                self.img = img
                for predResult in predResults:
                        if predResult['cls'] == self.class2Index[self.class_]:
                                position = [predResult['leftTop'], predResult['rightBottom']]
                                position = [
                                        (position[0][0] / 2, position[0][1] / 2),
                                        (position[1][0] / 2, position[1][1] / 2)
                                ]
                                icon = CoordinateIcon(position=position)
                                self._icons.append(icon)
                return self._icons

        def showImg(self):
                tool.imshow(self.img)

startGameIcon = Icon('img/base/start_game.png')

notificationPageDownBar = Icon('img/notificationDownBar.png')

kuloNoSuOccurPageLocator = Icon('img/kuloNoSuOccurPage.png')
kuloNoSuOccurPageGoTo = Icon('img/kuloNoSuOccurGoTo.png')

diagLogNextIcon = Icon('img/diagLogNextIcon.png')
diagLogBackground = Icon('img/diagLogBackground.png')
diagLogTitleIcon = Icon('img/diagLogTitleIcon.png')

getSaiFragment = Icon('img/getSaiFragments.png')
