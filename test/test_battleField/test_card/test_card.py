import sys
import os
from PIL.Image import HAMMING
thisFile = __file__
sys.path.append(os.path.dirname(os.path.dirname(thisFile)))

import cv2 as cv
import pytest

from card import CardCollection
from const import CARD_DICT_FILE
from battleField import BattleField, Area

cardCollection = CardCollection(CARD_DICT_FILE)

class TestCard:

    @pytest.mark.parametrize('imgPath,cardName,area,exists', [
        ('test/test_battleField/test_card/screenshot1.png', '蓝药水', Area.HAND, True),
        ('test/test_battleField/test_card/screenshot2.png', '蓝药水', Area.GRAVE, True),
        ('test/test_battleField/test_card/screenshot3.png', '蓝药水', Area.HAND, True),
        ('test/test_battleField/test_card/screenshot4.png', '蓝药水', Area.HAND, True),
        ('test/test_battleField/test_card/screenshot5.png', '守墓的随从', Area.HAND, True),
        # ('te/test_battleField/t/test_card/screenshot6.png',  '行者哥布林', Area.GRAVE, True),
        ('test/test_battleField/test_card/screenshot9.png', '守墓的随从', Area.HAND, True),
        ('test/test_battleField/test_card/screenshot5.png', '蓝药水', Area.GRAVE, False),
        ('test/test_battleField/test_card/screenshot8.png', '魔导兽 刻耳柏洛斯', Area.MONSTER, True),
        ('test/test_battleField/test_card/screenshot9.png', '魔导兽 刻耳柏洛斯', Area.MONSTER, True),
        ('test/test_battleField/test_card/screenshot10.png', '不屈斗士 磊磊', Area.HAND, False)
    ])
    def test_where(self, imgPath, cardName, area, exists):
        background = cv.imread(imgPath)
        battleField = BattleField(background)
        card = cardCollection.getCardByName(cardName)
        icon = battleField.detectArea(card, area)
        if exists: 
            assert icon is not None
        else:
            assert icon is None