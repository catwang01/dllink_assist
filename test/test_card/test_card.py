import sys
import os
thisFile = __file__
sys.path.append(os.path.dirname(os.path.dirname(thisFile)))

import cv2 as cv
import pytest

from card import CardCollection
from const import CARD_DICT_FILE

cardCollection = CardCollection(CARD_DICT_FILE)

class TestCard:

    @pytest.mark.parametrize('imgPath,cardName,area', [
        ('test/test_card/screenshot1.png', '蓝药水', 'hand'),
        ('test/test_card/screenshot3.png', '蓝药水', 'hand'),
        ('test/test_card/screenshot4.png',  '蓝药水', 'hand'),
        ('test/test_card/screenshot4.png',  '蓝药水', 'hand'),
        ('test/test_card/screenshot5.png', '守墓的随从', 'hand'),
        ('test/test_card/screenshot6.png',  '行者哥布林', 'grave'),
        ('test/test_card/screenshot9.png', '守墓的随从', 'hand'),
    ])
    def test_where(self, imgPath, cardName, area):
        img_scene = cv.imread(imgPath)

        card = cardCollection.getCardByName(cardName)
        assert card.exists(img_scene=img_scene, init=True, showImg=False)
        assert card.area == area


    @pytest.mark.parametrize('imgPath, cardName, expected',
    [
        ('test/test_card/screenshot5.png', '蓝药水', False),
        ('test/test_card/screenshot8.png', '魔导兽 刻耳柏洛斯', True)
    ])
    def test_where_whether_exists(self, imgPath, cardName, expected):
        img_scene = cv.imread(imgPath)
        card = cardCollection.getCardByName(cardName)
        assert card.exists(img_scene=img_scene, init=True) == expected

    def test_where_2(self):
        imgPath = 'test/test_card/screenshot2.png'
        img_scene = cv.imread(imgPath)
        card = cardCollection.getCardByName('魔导兽 刻耳柏洛斯')
        assert card.exists(img_scene=img_scene, init=True)
        assert card.area == 'monster'

        card = cardCollection.getCardByName('联合攻击')
        card.init(img_scene=img_scene)
        assert card.area == 'hand'

        card = cardCollection.getCardByName('行者哥布林')
        assert not card.exists(img_scene=img_scene, init=True)

        card = cardCollection.getCardByName('蓝药水')
        card.init(img_scene=img_scene)
        assert card.area == 'grave'
