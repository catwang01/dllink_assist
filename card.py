import os
import logging

import cv2 as cv
import numpy as np
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
from log.log import setupLogging

import tool
from icons import CoordinateIcon
from tool import get_appshot, Timer

setupLogging()

def computeArea(points):
    return Polygon(points).area

def checkParallel(points, threshold):
    line1 = np.array(points[0]) - np.array(points[1])
    line2 = np.array(points[-1]) - np.array(points[-2])
    # diff = np.sqrt(np.sum(np.square(line1 - line2))) 
    cosine = np.sum(line1 * line2) / (np.sqrt(np.sum(line1 ** 2) * np.sum(line2 ** 2)))
    theta = np.abs(np.arccos(cosine))
    return np.isclose(theta, 0, atol=threshold)

def checkVertical(points, threshold):
    line1 = np.array(points[0]) - np.array(points[1])
    line2 = np.array(points[0]) - np.array(points[-1])
    # diff = np.sqrt(np.sum(np.square(line1 - line2))) 
    cosine = np.sum(line1 * line2) / (np.sqrt(np.sum(line1 ** 2) * np.sum(line2 ** 2)))
    theta = np.abs(np.arccos(cosine))
    return np.isclose(theta, np.pi / 2, atol=threshold)

def isValidCard(points, threshold=None):
    if threshold is None:
        threshold = 1 / np.pi
    polygonArea = computeArea(points)
    if polygonArea < 6000 or polygonArea > 50000:
        return False
    return  checkParallel(points, threshold) and \
            checkVertical(points, threshold) and \
            checkParallel(points[1:] + [points[0]], threshold)

def checkInit(func):
    def wrapped(*args, **kwargs):
        cls = args[0]
        if not cls.isInitiated:
            raise Exception('CardCollection not initiated!')
        return func(*args, **kwargs)
    return wrapped

class CardCollection:

    def __init__(self, configFile) -> None:
        self.isInitiated = False
        self.name2code = {}
        self.code2name = {}
        self.init(configFile)

    def init(self, configFile):
        if not os.path.exists(configFile):
            raise Exception(f"configFile {configFile} does not exist!")
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

    def __init__(self, path, name=None) -> None:
        self.path = path
        self.name = name
        self.img = cv.imread(path)

    def __repr__(self) -> str:
        return f"Card(name='{self.name}', path='{self.path}')"

    def show(self):
        plt.imshow(self.img)
        plt.show()


class CardPlaceholder:

    def __init__(self, position) -> None:
        self.position = position
        self.icon = CoordinateIcon(position=position)

    def click(self):
        return self.icon.click()