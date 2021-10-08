import sys
import os
thisFile = __file__
sys.path.append(os.path.dirname(os.path.dirname(thisFile)))

import cv2 as cv
import pytest

from card import CardCollection

class TestCard:

    @pytest.mark.parametrize('imgPath', [
        'test/test_card/screenshot1.png',
        'test/test_card/screenshot3.png',
        'test/test_card/screenshot4.png',
    ])
    def test_where(self, imgPath):
        img_scene = cv.imread(imgPath)
        cardCollection = CardCollection()
        cardCollection.init()

        card = cardCollection.getCardByName('蓝药水')
        assert card.exists(img_scene=img_scene, init=True)
        assert card.area == 'hand'

    def test_where_2(self):
        imgPath = 'test/test_card/screenshot2.png'
        img_scene = cv.imread(imgPath)
        cardCollection = CardCollection()
        cardCollection.init()

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

    def test_where_3(self):
        imgPath = 'test/test_card/screenshot5.png'
        img_scene = cv.imread(imgPath)
        cardCollection = CardCollection()
        cardCollection.init()

        card = cardCollection.getCardByName('守墓的随从')
        assert card.exists(img_scene=img_scene, init=True)
        assert card.area == 'hand'
