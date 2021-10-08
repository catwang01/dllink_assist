from enum import Enum

from icons import CoordinateIcon
from matplotlib import pyplot as plt
import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np

import tool

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

def extractNumber(img_, templates, showImg=False):
    # 提取指定画面中的数字轮廓   
    img = img_.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    _, contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # plt.hist(gray.ravel())
    # plt.imshow(img)
    result = []
    for cnt in contours:
        [x,y,w,h] = cv2.boundingRect(cnt)
        # filter by w, h
        if 20 <= h <= 30 and 10 <= w <= 30:
            result.append([x,y,w,h])
    result.sort(key=lambda x:x[0])

    predictVals = []
    for x, y, w, h in result:
        # 在画面中标记识别的结果                
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,0,255), 1)
        digit = cv2.resize(thresh[y:y+h, x:x+w], (20, 25))
        # digit = cv2.resize(gray[y:y+h, x:x+w], (20, 25))
        res = []
        for i, t in enumerate(templates):
            score = cv2.matchTemplate(digit, t, cv2.TM_SQDIFF_NORMED)
            minScore = cv2.minMaxLoc(score)[0]
            res.append((i, minScore))
        res.sort(key=lambda x:x[1])
        _, contours, _ = cv2.findContours(digit, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if {res[0][0], res[1][0]} == {3, 8}:
            if len(contours) == 2:
                predictVal = 3
            else:
                predictVal = 8
        # elif res[0][0] == 1:
        #     # test = digit.copy()
        #     # cv2.drawContours(test, contours, -1, (127,127), 1)
        #     # tool.imshow(test)
        #     # len(contours)
        #     # cv2.contourArea(contours[0])
        #     # cv2.contourArea(contours[1])
        #     if len(contours) == 2:
        #         predictVal = 1
        #     else:
        #         continue
        else:
            if res[0][1] < 0.5:
                predictVal = res[0][0]
            else:
                continue
        # print(predictVal, res)
        predictVals.append(predictVal)
        cv2.putText(img, str(f"{predictVal}"), (x, y+35), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1)
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
            icon = CoordinateIcon([(359, 469), (415, 556)])
        elif direc == Direction.RIVAL:
            icon = CoordinateIcon([(58, 129), (105, 197)])
        else:
            raise Exception(f"No such item in {Direction}")
        img = icon.showImg(self.background)
        numbers = extractNumber(img, getTemplateImages(None), showImg=False)
        if numbers == '':
            return 0
        return int(numbers)