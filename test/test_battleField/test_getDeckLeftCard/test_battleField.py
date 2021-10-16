import sys
import os
thisFile = __file__
sys.path.append(os.path.dirname(os.path.dirname(thisFile)))

import pytest

from battleField import BattleField, Direction

import cv2 as cv
import pytest

from card import CardCollection
from const import CARD_DICT_FILE
from battleField import BattleField, Area

cardCollection = CardCollection(CARD_DICT_FILE)

class TestBattleField:

    @pytest.mark.parametrize("imgPath,expected1,expected2", [
        ('test/test_battleField/test_getdeckLeftCard/screenshot1.png', 9, 10),
        ('test/test_battleField/test_getdeckLeftCard/screenshot2.png', 15, 16),
        ('test/test_battleField/test_getdeckLeftCard/screenshot3.png', 8, 9),
        ('test/test_battleField/test_getdeckLeftCard/screenshot4.png', 7, 8),
        ('test/test_battleField/test_getdeckLeftCard/screenshot5.png', 11, 12),
        ('test/test_battleField/test_getdeckLeftCard/screenshot6.png', 8, 9),
        ('test/test_battleField/test_getdeckLeftCard/screenshot7.png', 1, 2),
        ('test/test_battleField/test_getdeckLeftCard/screenshot8.png', 0, 1),
        ('test/test_battleField/test_getdeckLeftCard/screenshot9.png', 1, 1),
        ('test/test_battleField/test_getdeckLeftCard/screenshot10.png', 0, 1),
        ('test/test_battleField/test_getdeckLeftCard/screenshot11.png', 6, 7),
        ('test/test_battleField/test_getdeckLeftCard/screenshot12.png', 1, 2),
        ('test/test_battleField/test_getdeckLeftCard/screenshot13.png', 0, 1),
        ('test/test_battleField/test_getdeckLeftCard/screenshot14.png', 0, 1),
    ])
    def test_getDeckLeftCard(self, imgPath, expected1, expected2):
        bf = BattleField(imgPath)
        assert bf.nGetDeckLeftCard() == expected1
        assert bf.nGetDeckLeftCard(direc=Direction.RIVAL) == expected2

