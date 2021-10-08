import cv2 as cv
import numpy as np
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
import logging
from log.log import setupLogging

import tool
from icons import CoordinateIcon
from tool import get_appshot, Timer

setupLogging()

def computeArea(points):
    return Polygon(points).area

def isValidCard(points, threshold=None):
    if threshold is None:
        threshold = 1 / np.pi
    polygonArea = computeArea(points)
    if  polygonArea < 6000 or polygonArea > 50000:
        return False
    line1 = np.array(points[0]) - np.array(points[1])
    line2 = np.array(points[-1]) - np.array(points[-2])
    # diff = np.sqrt(np.sum(np.square(line1 - line2))) 
    cosine = np.sum(line1 * line2) / (np.sqrt(np.sum(line1 ** 2) * np.sum(line2 ** 2)))
    diff = np.abs(np.arccos(cosine))
    logging.debug(f"diff: {diff:1.3} threshold: {threshold:1.3} result: {diff < threshold}")
    return diff < threshold

def checkInit(func):
    def wrapped(*args, **kwargs):
        cls = args[0]
        if not cls.isInitiated:
            raise Exception('CardCollection not initiated!')
        return func(*args, **kwargs)
    return wrapped

class CardCollection:


    def __init__(self) -> None:
        self.isInitiated = False
        self.name2code = {}
        self.code2name = {}

    def init(self, configFile='img/cards/cardMap.txt'):
        with open(configFile) as f:
            for line in f:
                line = line.strip()
                name, code = line.split(',')
                self.name2code[name] = code
                self.code2name[code] = name
        self.isInitiated = True
        return self

    @checkInit
    def getCardByName(self, name):
        code = self.name2code[name]
        return Card(path=f'img/cards/{code}.png', name=name)

    @checkInit
    def getCardByCode(self, code):
        name = self.code2name[code]
        return Card(path=f'img/cards/{code}.png', name=name)


class Card:

    detector = cv.xfeatures2d.SIFT_create()

    def __init__(self, path, name=None) -> None:
        self.path = path
        self.name = name
        self.img = cv.imread(path, cv.IMREAD_GRAYSCALE)
        self._points = None
        self.icon = None

    @property
    def points(self):
        if self._points is None:
            raise Exception(f"Card {self} can't be found!")
        return self._points

    def __repr__(self) -> str:
        return f"Card(name='{self.name}', path='{self.path}', area='{self.area}')"

    def init(self, *args, **kwargs):
        self._points = self.detect(*args, **kwargs)
        if self._points is not None:
            self.icon = CoordinateIcon([
                (self.points[0][0]/2, self.points[0][1]/2), 
                (self.points[2][0]/2, self.points[2][1]/2)
            ])
            logging.debug(f"{self} initiated")
        else:
            self.icon = None
            logging.warning(f"{self} doesn't exists")

    def exists(self, init=False, *args, **kwargs):
        if init:
            self.init(*args, **kwargs)
        return self._points is not None

    def show(self):
        plt.imshow(self.img)
        plt.show()

    def detect(self, img_scene=None, threshold=None, *args, **kwargs):
        img_object = self.img
        if img_scene is None:
            img_scene = get_appshot()
        with Timer('find_img_by_descriptor', stdout=logging.debug):
            scene_corners  = tool.find_img_by_descriptor(
                img_object, img_scene, detector=self.detector, *args, **kwargs
            )
        if scene_corners is None:
            return None
        points = scene_corners.squeeze().tolist()
        if not isValidCard(points, threshold):
            return None
        return points

    def click(self):
        return self.icon.click(x=-10)

    def drag(self, endPoint=(200, 300)):
        curPosition = self.click()
        tool.Operation().slide(curPosition, endPoint)

    @property
    def area(self):
        if self.icon is None:
            return None
        w = self.icon.position[0][0] / 2
        h = self.icon.position[0][1] / 2
        position = None
        if h > 580:
            position = 'hand'
        elif 460 < h <= 540:
            position = 'spell'
        elif 340 < w <= 390 and 350 < h <= 430:
            position = 'grave'
        elif 365 < h <= 455:
            position = 'monster'
        else:
            logging.warning(f'w,h={w},{h} not falls in one category!')
            # raise Exception(f'h = {h} not falls in one category!')
        return position


class CardPlaceholder:

    def __init__(self, position) -> None:
        self.position = position
        self.icon = CoordinateIcon(position=position)

    def click(self):
        return self.icon.click()