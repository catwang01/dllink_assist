import pytest
import cv2

from homepage.icons import unionForceIcon
from unionForce.icons import unionForceChallengeButton, unionForceTitle

class TestUnionForce:

    @pytest.mark.parametrize('imgPath,icon,expected', 
        [
            ('test/test_unionForce/screenshot1.png', unionForceIcon, True),
            ('test/test_unionForce/screenshot2.png', unionForceIcon, True),
            ('test/test_unionForce/screenshot3.png', unionForceChallengeButton, False),
            ('test/test_unionForce/screenshot4.png', unionForceTitle, False),
            ('test/test_unionForce/screenshot5.png', unionForceChallengeButton, True),
        ]
    )
    def testUnionForceIcon(self, imgPath, icon, expected):
        icon.background = cv2.imread(imgPath)
        assert icon.exists() == expected