from enum import Enum
import logging

import cv2
from matplotlib import pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import numpy as np

from icons import CoordinateIcon
from log.log import setupLogging
import tool

setupLogging()

def draw_png(name, font_file, font_size = 36):
    font=ImageFont.truetype(font_file, font_size)
    text_width, text_height = font.getsize(name)
    image = Image.new(mode='RGB', size=(text_width, text_height))
    draw_table = ImageDraw.Draw(im=image)
    draw_table.text(xy=(0, -3), text=name, font=font)

    # convert image into binary format
    imageArray = cv2.cvtColor(np.array(image, dtype=np.uint8), cv2.COLOR_BGR2GRAY)
    imageArray = 255 - imageArray
    return imageArray

def getTemplateImages(font):
    templates = []
    for i in range(10):
        image = draw_png(str(i), font_file='华康新综艺体W7-P.ttf')
        templates.append(image)
    return templates

def boxNumber(img):
    img = img.copy()
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
    ret, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV |cv2.THRESH_TRUNC)
    # tool.imshow(thresh)
    mask = thresh > 180
    thresh[mask] = 255
    thresh[1 - mask] = 0
    _, contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    return contours, thresh

def getMinScore(digit, i, template):
    try:
        score = cv2.matchTemplate(digit, template, cv2.TM_SQDIFF_NORMED)
    except Exception:
        logging.warning(f'template {i} is larger than img! matchTemplate can\'t be performed')
    else:
        minScore = cv2.minMaxLoc(score)[0]
    return minScore

def extractNumber(img, templates, showImg=False):
    # 提取指定画面中的数字轮廓   
    contours, thresh = boxNumber(img)
    result = []
    for cnt in contours:
        [x,y,w,h] = cv2.boundingRect(cnt)
        # filter by w, h
        if 20 <= h <= 30 and 5 <= w <= 30:
            result.append([x,y,w,h])
    # sort by x coordinate
    result.sort(key=lambda x:x[0]) 

    processedTemplates = [0] * 10
    for i, template in enumerate(templates):
        template = 255 - template
        contours, tempThresh = boxNumber(template)
        contour = max(contours, key=lambda x: cv2.contourArea(x))
        x,y,w,h = cv2.boundingRect(contour)
        processedTemplates[i] = tempThresh[y:y+h, x:x+w]

    predictVals = []
    for x, y, w, h in result:
        # 在画面中标记识别的结果                
        padding = 8
        cv2.rectangle(img, (x-padding,y-padding), (x+w+padding,y+h+padding), (0,0,255), 1)
        height, width = thresh.shape
        digit = thresh[max(y-padding, 0):min(y+h+padding, height), max(x-padding, 0):min(x+w+padding, width)]
        _, contours, _ = cv2.findContours(digit, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        nContours = len(contours)
        contourDict = {
            1: [1, 2, 3, 5, 7],
            2: [0, 4, 6, 9],
            3: [8]
        }
        res = []
        for i in contourDict[nContours]:
            score = getMinScore(digit, i, processedTemplates[i])
            res.append((i, score))
        res.sort(key=lambda x:x[1])
        if len(res) == 0: continue
        predictVal = None
        if res[0][1] < 0.5:
            predictVal = res[0][0]
        if predictVal is not None:
            predictVals.append(predictVal)
            cv2.putText(img, str(f"{predictVal}"), (x, y+25), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1)
    if showImg:
        tool.imshow(img)
        plt.show()
    return ''.join(map(str, predictVals))

class Direction(Enum):
    SELF = 0
    RIVAL = 1

class BattleField:

    def __init__(self, background=None) -> None:
        if background is None:
            background = tool.get_appshot()
        elif isinstance(background, str):
            background = cv2.imread(background)
        self.background =  background

    def nGetDeckLeftCard(self, direc=Direction.SELF):
        numbers = None
        if direc == Direction.SELF:
            icon = CoordinateIcon([(370, 496), (405, 530)])
        elif direc == Direction.RIVAL:
            icon = CoordinateIcon([(55, 150), (95, 186)])
        else:
            raise Exception(f"No such item in {Direction}")
        icon.background = self.background
        img = icon.getImg()
        numbers = extractNumber(img, getTemplateImages(None), showImg=False)
        if numbers == '':
            return 0
        return int(numbers)