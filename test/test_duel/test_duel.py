import os
thisDir = os.path.dirname(os.path.abspath(__file__))
import pytest
import cv2

from duel.icons import settingButton, duelButton

class TestDuel:

    @pytest.mark.parametrize("imgPath,expectedVal", [
        (f'{thisDir}/test1.png', True),
        (f'{thisDir}/test2.png', True),
        (f'{thisDir}/test3.png', False),
    ])
    def test_settingButton(self, imgPath, expectedVal):
        img = cv2.imread(imgPath)
        settingButton.background = img
        assert settingButton.exists() == expectedVal

    @pytest.mark.parametrize('imgPath,expectedVal', [
        (f'{thisDir}/test4.png', True)
    ])
    def test_duelButton(self, imgPath, expectedVal):
        img = cv2.imread(imgPath)
        duelButton.background = img
        assert duelButton.exists() == expectedVal

    
