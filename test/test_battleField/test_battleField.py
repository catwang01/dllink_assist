import sys
import os
thisFile = __file__
sys.path.append(os.path.dirname(os.path.dirname(thisFile)))

import pytest

from battleField import BattleField, Direction

class TestBattleField:

    @pytest.mark.parametrize("imgPath,expected1,expected2", [
        ('test/test_battleField/screenshot1.png', 9, 10),
        ('test/test_battleField/screenshot2.png', 15, 16),
        ('test/test_battleField/screenshot3.png', 8, 9),
        ('test/test_battleField/screenshot4.png', 7, 8),
        ('test/test_battleField/screenshot5.png', 11, 12),
        ('test/test_battleField/screenshot6.png', 8, 9),
        ('test/test_battleField/screenshot7.png', 1, 2),
        ('test/test_battleField/screenshot8.png', 0, 1),
        ('test/test_battleField/screenshot9.png', 1, 1),
    ])
    def test_getDeckLeftCard(self, imgPath, expected1, expected2):
        bf = BattleField(imgPath)
        assert bf.nGetDeckLeftCard() == expected1
        assert bf.nGetDeckLeftCard(direc=Direction.RIVAL) == expected2
