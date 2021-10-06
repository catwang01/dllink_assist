import sys
import os
thisFile = __file__
sys.path.append(os.path.dirname(os.path.dirname(thisFile)))
from battleField import BattleField, Direction

class TestBattleField:

    def test_getDeckLeftCard(self):
        bf = BattleField('test/test_battleField/screenshot2.png')
        assert bf.nGetDeckLeftCard() == '15'
        assert bf.nGetDeckLeftCard(direc=Direction.RIVAL) == '16'
